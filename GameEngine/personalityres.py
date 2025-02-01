# contains personality csv and results from ai 

# saving and editing the csv file

class player_sheet():
    
    def __init__(self, blank_sheet_path):
        import csv
        with open(blank_sheet_path, encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            self.player_sheet = [row for row in reader]

        self.personality_dict = {'Agreeableness':[],
                                 'Openness':[],
                                 'Neuroticism':[],
                                 'Conscientiousness':[],
                                 'Extraversion':[]}

    def check_for_missing_values(self):
        return_list = []
        for row in self.player_sheet:
            if row["Score"] == "":
                return_list.append(row["Question"])
        return return_list
    
    def update_player_sheet(self):
        pass
    
    def _load_traits_(self):
        for row in self.player_sheet:
            if row["Reverse?"] == "N":
                self.personality_dict[row["Trait"]].append(float(row["Score"]))
            else:
                self.personality_dict[row["Trait"]].append(6 - float(row["Score"]))
    
    def print_traits(self):
        if self.personality_dict["Agreeableness"] == []:
            self._load_traits_()
        else:
            for key,val in self.personality_dict.items():
                print(f"{key}: {sum(val) / len(val)}")

    def print_personality_type(self):
        pass
        #What weightings lead to what type...

p1 = player_sheet('csv/BFI_44.csv')
print(p1.player_sheet)
print(p1.check_for_missing_values())