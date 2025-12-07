from dataclasses import dataclass
import io

@dataclass
class IngredientIdRange:
    lowerbound: int
    upperbound: int

    def falls_within_range(self, ingredient_id: int) -> bool:
        return (self.lowerbound <= ingredient_id) and (self.upperbound >= ingredient_id)

def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    reading_ranges = True
    good_ingredient_ranges = []
    ingredient_count = 0
    spoiled_ingredient_count = 0
    for line in lines:
        if line == "\n":
            reading_ranges = False
        elif reading_ranges:
            line = line.replace("\n", "")
            lb, ub = map(int, line.split("-"))
            good_ingredient_ranges.append(IngredientIdRange(lb, ub))
        else:
            line = line.replace("\n", "")
            ingredient_count += 1
            ingredient_to_check = int(line)
            for ingredient_range in good_ingredient_ranges:
                if ingredient_range.falls_within_range(ingredient_to_check):
                    break
            else:
                spoiled_ingredient_count += 1
    return ingredient_count - spoiled_ingredient_count





def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
