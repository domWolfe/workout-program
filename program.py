import random
#Chest Exercises
#Programs will follow a system
#Choose from heavy exercises 1x
#2 pushing movements, 2 fly movements
#Upper Chest Must be Hit by at least One Exercise

class Exercise:
    def __init__(self, name, type, link=""):
        self.name = name
        self.type = type
        self.link = link
    
    def print_exercise(self):
        print(f"Exercise: {self.name}, Type: {self.type}, Link: {self.link}")

class ExerciseList:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def add_exercise_by_con(self, name, type, link=""):
        self.exercises.append(Exercise(name, type, link))

    def get_exercises_by_type(self, type) -> list:
        return [exercise for exercise in self.exercises if exercise.type == type]
    
# 0 = Regular Press, 1 = Upper Chest Press, 2 = Regular Fly, 3 = Upper Chest Fly
# 0 = Heavy Tricep Lateral, 1 = Heavy Tricep Long, 2 = Tricep Pushdown Variation, 3 = Tricep Overhead Variation

chest_exercises = ExerciseList()
chest_exercises.add_exercise_by_con("Flat Barbell Bench Press", 0)
chest_exercises.add_exercise_by_con("Flat Dumbbell Bench Press", 0)
chest_exercises.add_exercise_by_con("Incline Barbell Bench Press", 1)
chest_exercises.add_exercise_by_con("Incline Dumbbell Bench Press", 1)
chest_exercises.add_exercise_by_con("Incline Smith Machine Press", 1)
chest_exercises.add_exercise_by_con("Incline Machine Press", 1)
chest_exercises.add_exercise_by_con("Standing Cable Fly", 2)
chest_exercises.add_exercise_by_con("Machine Cable Fly (Pec Deck)", 2)
chest_exercises.add_exercise_by_con("Decline Cable Fly", 2)
chest_exercises.add_exercise_by_con("Low to High Cable Fly", 3)

triceps_exercises = ExerciseList()
triceps_exercises.add_exercise_by_con("Close Grip Bench Press", 0)
triceps_exercises.add_exercise_by_con("Weighted Dips", 0)
triceps_exercises.add_exercise_by_con("Machine Dips", 0)
triceps_exercises.add_exercise_by_con("Skull Crushers", 1)
triceps_exercises.add_exercise_by_con("JM Press", 1)
triceps_exercises.add_exercise_by_con("Rope Tricep Pushdown", 2)
triceps_exercises.add_exercise_by_con("Straight Bar Tricep Pushdown", 2)
triceps_exercises.add_exercise_by_con("V-Bar Tricep Pushdown", 2)
triceps_exercises.add_exercise_by_con("Overhead Dumbbell Tricep Extension", 3)
triceps_exercises.add_exercise_by_con("Overhead Cable Tricep Extension", 3)
triceps_exercises.add_exercise_by_con("Single Arm Overhead Cable Tricep Extension", 3)
triceps_exercises.add_exercise_by_con("Single Arm Overhead Dumbbell Tricep Extension", 3)

class WorkoutExercises:
    def __init__(self, exercise_list):
        self.exercise_list = exercise_list
        self.program = {}

    def generate_exercises(self):
        program = []
        heavy_exercises = self.exercise_list.get_exercises_by_type(0) + self.exercise_list.get_exercises_by_type(1)
        program.append(random.choice(heavy_exercises))
        type_chosen = program[0].type
        program.append(random.choice(self.exercise_list.get_exercises_by_type(1-type_chosen)))
        secondary_exercises = self.exercise_list.get_exercises_by_type(2) + self.exercise_list.get_exercises_by_type(3)
        program.append(random.choice(secondary_exercises))
        second_light = random.choice(secondary_exercises)
        while second_light.type in [exercise.type for exercise in program]:
            second_light = random.choice(secondary_exercises)
        program.append(second_light)
        return program
    
#Multiple Different Ways to Generate a Program
    # Push Pull Legs 2x a Week (0)
    # Upper Lower 2x a Week (1)
    # Chest/Back Arms Legs 2x a Week (2)
    # Full Body 3x a Week (3)
class WorkoutProgram:
    def __init__(self, program_type):
        self.program_type = program_type
        self.workouts = {}
    
    def generate_ppl_program(self):
        chest_workout = WorkoutExercises(chest_exercises)
        program_chest = chest_workout.generate_exercises()
        tricep_workout = WorkoutExercises(triceps_exercises)
        program_triceps = tricep_workout.generate_exercises()
        self.workouts["Push"] = program_chest + program_triceps

    def print_program(self):
        for workout_name, exercises in self.workouts.items():
            print(f"{workout_name} Workout:")
            for exercise in exercises:
                exercise.print_exercise()
            print()

ppl_program = WorkoutProgram(0)
ppl_program.generate_ppl_program()
ppl_program.print_program()