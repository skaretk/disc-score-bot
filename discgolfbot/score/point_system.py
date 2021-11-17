# Current score scheme for league, based on Disc Golf Pro Tour Points
# https://udisc.com/blog/post/how-disc-golf-pro-tour-points-work-why-they-matter

class PointSystem():
    # Get points based on scorecard position
    def get_points(position: int):
        return {
            0: 1,
            1: 100,
            2: 85,
            3: 75,
            4: 69,
            5: 64,
            6: 60,
            7: 57,
            8: 54,
            9: 52,
            10: 50,
            11: 48,
            12: 46,
            13: 44,
            14: 42,
            15: 40,
            16: 38,
            17: 36,
            18: 34,
            19: 32,
            20: 30,
            21: 29,
            22: 28,
            23: 27,
            24: 26,
            25: 25,
            26: 24,
            27: 23,
            28: 22,
            29: 21,
            30: 20,
            31: 19,
            32: 18,
            33: 17,
            34: 16,
            35: 15,
            36: 14,
            37: 13,
            38: 12,
            39: 11,
            40: 10,
            41: 9,
            42: 8,
            43: 7,
            44: 6,
            45: 5,
            46: 4,
            47: 3,
            48: 2,
            49: 2,
            50: 2
        }.get(position, 0)
    
    def calculate_scores(positions):
        points = 0
        for position in positions:
            points += PointSystem.get_points(position)
        return points
