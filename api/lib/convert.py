class converter:
    def __init__(self, param):
        self.param = param

    def state(state=None):
        # Convert state abbreviations to codes
        state_dict = {'AL': 1, 'AK': 2, 'AZ': 3, 'AR': 4, 'CA': 5, 'CO': 6,
                      'CT': 7, 'DE': 8, 'DC': 9, 'FL': 10, 'GA': 11, 'HI': 12,
                      'ID': 13, 'IL': 14, 'IN': 15, 'IA': 16, 'KS': 17,
                      'KY': 18, 'LA': 19, 'ME': 20, 'MD': 21, 'MA': 22,
                      'MI': 23, 'MN': 24, 'MS': 25, 'MO': 26, 'MT': 27,
                      'NE': 28, 'NV': 29, 'NH': 30, 'NJ': 31, 'NM': 32,
                      'NY': 33, 'NC': 34, 'ND': 35, 'OH': 36, 'OK': 37,
                      'OR': 38, 'PA': 39, 'RI': 41, 'SC': 42, 'SD': 43,
                      'TN': 44, 'TX': 45, 'UT': 46, 'VT': 47, 'VA': 49,
                      'WA': 50, 'WV': 51, 'WI': 52, 'WY': 53, 'OTHER': 54}

        try:
            state_code = state_dict[state.upper()]
        except Exception:
            state_code = 54
        return state_code

    def race(race):
        # Convert race to other if mistype or none
        if race not in (1, 2, 5):
            race = 3
        else:
            race
        return race

    def condition(self, condition=None):
        # Convert condition if none otherwise raise exception
        if condition is None:
            condition = 2
        elif condition not in (None, 1, 2):
            raise Exception('{} must be 1 or 2'.format(self.capitalize()))
        else:
            condition
        return condition

    def claims(self, claims=None):
        # Convert claims if none otherwise raise exception
        if claims is None:
            claims = 0
        elif type(claims) is not int:
            raise Exception('Number of {} must be a number'.format(self.upper()))
        else:
            claims
        return claims
