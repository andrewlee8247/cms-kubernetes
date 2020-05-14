import os
import requests
from bs4 import BeautifulSoup
import zipfile
import pandas as pd
import numpy as np
import pyarrow
import logging
from datetime import datetime
from google.cloud import storage
from google.cloud.storage import Blob


def tryRequest(url, headers):
    # Ping site until response status is 200, if not print fail
    success = False
    for _ in range(5):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            success = True
            return response
            break
        else:
            print("Response received: %s. Retrying: %s" % (response.status_code, url))
            success = False
    if success == False:
        return print("Failed to process the URL: ", url)


def parseFiles():
    st_time = datetime.now()  # Start time
    logging.basicConfig(filename="scrape.log", filemode="w", level=logging.DEBUG)
    logging.info("Data processing started at {}".format(st_time))

    storage_client = storage.Client()
    bucket_b = storage_client.get_bucket("cms-beneficiary")
    bucket_i = storage_client.get_bucket("cms-inpatient")
    bucket_l = storage_client.get_bucket("logs-cms")

    dir = "/processing/files/"
    url_path = "https://www.cms.gov"
    url = "https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF"
    headers = {"User-Agent": "Chrome/54.0.2840.90"}
    # Grab all href from file summary page
    response = tryRequest(url, headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    tmpRow = soup.findAll("a")
    count = 0

    for i in range(len(tmpRow)):
        # Extract all links to pages that have cms data files to download
        try:
            if tmpRow[i].contents[0].split(" ")[0] == "DE1.0":
                response = requests.get(url_path + tmpRow[i]["href"], headers=headers)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                tmpUrl = soup.findAll("a")
                for k in range(len(tmpUrl)):
                    # Download all files, transform, process into parquet files, and upload to cloud storage
                    # all files in container are then removed
                    try:
                        if tmpUrl[k].contents[0].split(" ")[4] == "Beneficiary":
                            filepath = tmpUrl[k]["href"]
                            try:
                                response = tryRequest(
                                    url_path + filepath, headers=headers
                                )
                                zip_path = dir + filepath.split("/")[-1]
                                with open(zip_path, "wb") as f:
                                    f.write(response.content)
                                filename = zipfile.ZipFile(zip_path, "r").namelist()[0]
                                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                    zip_ref.extractall(dir)
                                os.remove(zip_path)
                                df = pd.read_csv(dir + filename, low_memory=False)
                                os.remove(dir + filename)
                                df["BENE_BIRTH_DT"] = pd.to_datetime(
                                    df["BENE_BIRTH_DT"].astype(str), format="%Y%m%d"
                                ).dt.date
                                df["BENE_BIRTH_DT"].fillna(np.nan, inplace=True)
                                df["BENE_DEATH_DT"] = pd.to_datetime(
                                    df["BENE_DEATH_DT"].astype(str), format="%Y%m%d"
                                ).dt.date
                                df["BENE_DEATH_DT"].fillna(np.nan, inplace=True)
                                df = df.apply(
                                    lambda x: x.astype("int16")
                                    if x.dtype == "int64"
                                    else x
                                )
                                parq_file = filename.split(".")[0] + ".parquet"
                                df.to_parquet(dir + parq_file)
                                blob = Blob(parq_file, bucket_b)
                                with open(dir + parq_file, "rb") as my_file:
                                    blob.upload_from_file(my_file)
                                os.remove(dir + parq_file)
                                count += 1
                            except:
                                logging.info(response)
                        elif tmpUrl[k].contents[0].split(" ")[-3] == "Inpatient":
                            filepath = tmpUrl[k]["href"]
                            try:
                                response = tryRequest(
                                    url_path + filepath, headers=headers
                                )
                                zip_path = dir + filepath.split("/")[-1]
                                with open(zip_path, "wb") as f:
                                    f.write(response.content)
                                filename = zipfile.ZipFile(zip_path, "r").namelist()[0]
                                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                    zip_ref.extractall(dir)
                                os.remove(zip_path)
                                df = pd.read_csv(dir + filename, low_memory=False)
                                os.remove(dir + filename)
                                df["CLM_FROM_DT"] = pd.to_datetime(
                                    df["CLM_FROM_DT"].astype(str), format="%Y%m%d"
                                ).dt.date
                                df["CLM_FROM_DT"].fillna(np.nan, inplace=True)
                                df["CLM_THRU_DT"] = pd.to_datetime(
                                    df["CLM_THRU_DT"].astype(str), format="%Y%m%d"
                                ).dt.date
                                df["CLM_THRU_DT"].fillna(np.nan, inplace=True)
                                df["CLM_ADMSN_DT"] = pd.to_datetime(
                                    df["CLM_ADMSN_DT"].astype(str), format="%Y%m%d"
                                ).dt.date
                                df["CLM_ADMSN_DT"].fillna(np.nan, inplace=True)
                                df["NCH_BENE_DSCHRG_DT"] = pd.to_datetime(
                                    df["NCH_BENE_DSCHRG_DT"].astype(str),
                                    format="%Y%m%d",
                                ).dt.date
                                df["NCH_BENE_DSCHRG_DT"].fillna(np.nan, inplace=True)
                                df["AT_PHYSN_NPI"] = (
                                    df["AT_PHYSN_NPI"]
                                    .fillna(-1)
                                    .astype("int64")
                                    .astype(str)
                                    .replace("-1", np.nan)
                                )
                                df["OP_PHYSN_NPI"] = (
                                    df["OP_PHYSN_NPI"]
                                    .fillna(-1)
                                    .astype("int64")
                                    .astype(str)
                                    .replace("-1", np.nan)
                                )
                                df["OT_PHYSN_NPI"] = (
                                    df["OT_PHYSN_NPI"]
                                    .fillna(-1)
                                    .astype("int64")
                                    .astype(str)
                                    .replace("-1", np.nan)
                                )
                                df["SEGMENT"] = df["SEGMENT"].astype("int16")
                                df.iloc[:, 20:] = df.iloc[:, 20:].apply(
                                    lambda x: x.astype(str) if x.dtype == "float" else x
                                )
                                df["CLM_UTLZTN_DAY_CNT"] = (
                                    df["CLM_UTLZTN_DAY_CNT"].fillna(0).astype("int16")
                                )
                                parq_file = filename.split(".")[0] + ".parquet"
                                df.to_parquet(dir + parq_file)
                                blob = Blob(parq_file, bucket_i)
                                with open(dir + parq_file, "rb") as my_file:
                                    blob.upload_from_file(my_file)
                                os.remove(dir + parq_file)
                                count += 1
                            except:
                                logging.info(response)
                    except:
                        try:
                            if (
                                tmpUrl[k].contents[1].split("(", 1)[1].split(")")[0]
                                == "ZIP"
                            ):
                                if tmpUrl[k]["href"].split("_")[5] == "Inpatient":
                                    filepath = tmpUrl[k]["href"]
                                    try:
                                        response = tryRequest(
                                            url_path + filepath, headers=headers
                                        )
                                        zip_path = dir + filepath.split("/")[-1]
                                        with open(zip_path, "wb") as f:
                                            f.write(response.content)
                                        filename = zipfile.ZipFile(
                                            zip_path, "r"
                                        ).namelist()[0]
                                        with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                            zip_ref.extractall(dir)
                                        os.remove(zip_path)
                                        df = pd.read_csv(
                                            dir + filename, low_memory=False
                                        )
                                        os.remove(dir + filename)
                                        df["CLM_FROM_DT"] = pd.to_datetime(
                                            df["CLM_FROM_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["CLM_FROM_DT"].fillna(np.nan, inplace=True)
                                        df["CLM_THRU_DT"] = pd.to_datetime(
                                            df["CLM_THRU_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["CLM_THRU_DT"].fillna(np.nan, inplace=True)
                                        df["CLM_ADMSN_DT"] = pd.to_datetime(
                                            df["CLM_ADMSN_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["CLM_ADMSN_DT"].fillna(np.nan, inplace=True)
                                        df["NCH_BENE_DSCHRG_DT"] = pd.to_datetime(
                                            df["NCH_BENE_DSCHRG_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["NCH_BENE_DSCHRG_DT"].fillna(
                                            np.nan, inplace=True
                                        )
                                        df["AT_PHYSN_NPI"] = (
                                            df["AT_PHYSN_NPI"]
                                            .fillna(-1)
                                            .astype("int64")
                                            .astype(str)
                                            .replace("-1", np.nan)
                                        )
                                        df["OP_PHYSN_NPI"] = (
                                            df["OP_PHYSN_NPI"]
                                            .fillna(-1)
                                            .astype("int64")
                                            .astype(str)
                                            .replace("-1", np.nan)
                                        )
                                        df["OT_PHYSN_NPI"] = (
                                            df["OT_PHYSN_NPI"]
                                            .fillna(-1)
                                            .astype("int64")
                                            .astype(str)
                                            .replace("-1", np.nan)
                                        )
                                        df["SEGMENT"] = df["SEGMENT"].astype("int16")
                                        df.iloc[:, 20:] = df.iloc[:, 20:].apply(
                                            lambda x: x.astype(str)
                                            if x.dtype == "float"
                                            else x
                                        )
                                        df["CLM_UTLZTN_DAY_CNT"] = (
                                            df["CLM_UTLZTN_DAY_CNT"]
                                            .fillna(0)
                                            .astype("int16")
                                        )
                                        parq_file = filename.split(".")[0] + ".parquet"
                                        df.to_parquet(dir + parq_file)
                                        blob = Blob(parq_file, bucket_i)
                                        with open(dir + parq_file, "rb") as my_file:
                                            blob.upload_from_file(my_file)
                                        os.remove(dir + parq_file)
                                        count += 1
                                    except:
                                        logging.info(response)
                                elif tmpUrl[k]["href"].split("_")[3] == "Beneficiary":
                                    filepath = tmpUrl[k]["href"]
                                    try:
                                        response = tryRequest(
                                            url_path + filepath, headers=headers
                                        )
                                        zip_path = dir + filepath.split("/")[-1]
                                        with open(zip_path, "wb") as f:
                                            f.write(response.content)
                                        filename = zipfile.ZipFile(
                                            zip_path, "r"
                                        ).namelist()[0]
                                        with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                            zip_ref.extractall(dir)
                                        os.remove(zip_path)
                                        df = pd.read_csv(
                                            dir + filename, low_memory=False
                                        )
                                        os.remove(dir + filename)
                                        df["BENE_BIRTH_DT"] = pd.to_datetime(
                                            df["BENE_BIRTH_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["BENE_BIRTH_DT"].fillna(np.nan, inplace=True)
                                        df["BENE_DEATH_DT"] = pd.to_datetime(
                                            df["BENE_DEATH_DT"].astype(str),
                                            format="%Y%m%d",
                                        ).dt.date
                                        df["BENE_DEATH_DT"].fillna(np.nan, inplace=True)
                                        df = df.apply(
                                            lambda x: x.astype("int16")
                                            if x.dtype == "int64"
                                            else x
                                        )
                                        parq_file = filename.split(".")[0] + ".parquet"
                                        df.to_parquet(dir + parq_file)
                                        blob = Blob(parq_file, bucket_b)
                                        with open(dir + parq_file, "rb") as my_file:
                                            blob.upload_from_file(my_file)
                                        os.remove(dir + parq_file)
                                        count += 1
                                    except:
                                        logging.info(response)
                        except:
                            pass

        except:
            pass

    # Log completion
    fin_time = datetime.now()
    execution_time = fin_time - st_time
    logging.info("Data processing finished at {}".format(fin_time))
    logging.info("{} total files processed".format(count))
    logging.info("Total execution time: {}".format(str(execution_time)))

    # Upload log
    blob = Blob("scrape" + str(fin_time) + ".log", bucket_l)
    with open("/processing/scrape.log", "rb") as my_file:
        blob.upload_from_file(my_file)

    return
