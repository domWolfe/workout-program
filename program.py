import copy
import random
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class Exercise:
    def __init__(self, name, type, link=""):
        self.name = name
        self.type = type
        self.link = link
        self.base_sets = 2
        self.sets = 2
        if type in (0, 1):
            self.base_reps = "4-6"
        else:
            self.base_reps = "6-8"

        self.reps = self.base_reps

    #Will add progression to make it scale for larger week ranges
    def apply_progression(self, week):
        adjusted_week = week % 5
        if week == 3:
            self.sets = min(self.base_sets + 1, 4)
            low, high = map(int, self.base_reps.split("-"))
            self.reps = f"{low+1}-{high+1}"
        elif week > 3 and week <= 4:
            self.sets = min(self.base_sets + 1, 4)
            low, high = map(int, self.base_reps.split("-"))
            self.reps = f"{low+2}-{high+2}"
    
    def print_exercise(self):
        print(f"Exercise: {self.name}, Type: {self.type}, Volume: {self.sets}x{self.reps}, Link: {self.link}")

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
# 0 = Heavy Rowing Movement, 1 = Heavy Pulling Movement, 2 = Close Grip Rowing Movement, 3 = Traps
# 0 = Heavy Curls Long, 1 = Heavy Curls Short, 2 = Light Curls Long, 3 = Light Curls Short
# 0 = Heavy Squat, 1 = Heavy Hinge, 2 = Light Squat/Hinge, 3 = Accessory Lower Body
# 0 = Heavy Shoulder Press, 1 = Raise Variation, 2 = Rear Delt Variation, 3 = Calfs

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

back_exercises = ExerciseList()
back_exercises.add_exercise_by_con("Bent Over Barbell Rows", 0)
back_exercises.add_exercise_by_con("Bent Over Dumbbell Rows", 0)
back_exercises.add_exercise_by_con("Chest-Supported T-Bar Rows", 0)
back_exercises.add_exercise_by_con("Weighted Pull-Ups", 1)
back_exercises.add_exercise_by_con("Wide-Grip Lat-Pulldowns", 1)
back_exercises.add_exercise_by_con("Seated Cable Row", 2)
back_exercises.add_exercise_by_con("Seated Cable Row (V-Bar)", 2)
back_exercises.add_exercise_by_con("Face Pulls", 3)
back_exercises.add_exercise_by_con("Shrugs", 3)

bicep_exercises = ExerciseList()
bicep_exercises.add_exercise_by_con("Ez-Bar Curls", 0)
bicep_exercises.add_exercise_by_con("Dumbbell Curls", 0)
bicep_exercises.add_exercise_by_con("Preacher Curls", 1)
bicep_exercises.add_exercise_by_con("Cable Curls", 2)
bicep_exercises.add_exercise_by_con("Reverse Barbell Curls", 2)
bicep_exercises.add_exercise_by_con("Incline Dumbbell Curls", 2)
bicep_exercises.add_exercise_by_con("Hammer Curls", 2)
bicep_exercises.add_exercise_by_con("Spider Curls", 3)
bicep_exercises.add_exercise_by_con("Wide-Grip Ez-Bar Curls", 3)

leg_exercises = ExerciseList()
leg_exercises.add_exercise_by_con("Barbell Back Squat", 0)
leg_exercises.add_exercise_by_con("Front Squat", 0)
leg_exercises.add_exercise_by_con("Goblet Squat", 0)
leg_exercises.add_exercise_by_con("Romanian Deadlift", 1)
leg_exercises.add_exercise_by_con("Conventional Deadlift", 1)
leg_exercises.add_exercise_by_con("Leg Press", 2)
leg_exercises.add_exercise_by_con("Lunges", 2)
leg_exercises.add_exercise_by_con("Leg Extensions", 3)
leg_exercises.add_exercise_by_con("Leg Curls", 3)

shoulder_exercises = ExerciseList()
shoulder_exercises.add_exercise_by_con("Overhead Barbell Press", 0)
shoulder_exercises.add_exercise_by_con("Dumbbell Shoulder Press", 0)
shoulder_exercises.add_exercise_by_con("Lateral Raises", 1)
shoulder_exercises.add_exercise_by_con("Cable Lateral Raises", 1)
shoulder_exercises.add_exercise_by_con("Reverse Pec Deck Fly", 2)
shoulder_exercises.add_exercise_by_con("Bent Over Dumbbell Reverse Fly", 2)
shoulder_exercises.add_exercise_by_con("Face Pulls", 2)
shoulder_exercises.add_exercise_by_con("Calf Raises", 3)

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
    # Chest/Back Arms Legs 2x a Week (0)
    # Push Pull Legs 2x a Week (1)
    # Full Body 3x a Week (2)
    # Upper Lower 2x a Week (3)
class WorkoutProgram:
    def __init__(self, program_type):
        self.program_type = program_type
        self.workouts = {}
    
    def generate_program(self):
        if self.program_type == 0:
            self.generate_arnold_split()
        elif self.program_type == 1:
            self.generate_ppl_program()
        elif self.program_type == 2:
            self.generate_full_body_program()

    def generate_arnold_split(self):
        chest_workout = WorkoutExercises(chest_exercises)
        program_chest = chest_workout.generate_exercises()
        back_workout = WorkoutExercises(back_exercises)
        program_back = back_workout.generate_exercises()
        program_chest.sort(key=lambda x: x.type)
        program_back.sort(key=lambda x: x.type)
        self.workouts["Chest & Back"] = program_chest + program_back

        bicep_workout = WorkoutExercises(bicep_exercises)
        program_bicep = bicep_workout.generate_exercises()
        tricep_workout = WorkoutExercises(triceps_exercises)
        program_triceps = tricep_workout.generate_exercises()
        program_triceps.sort(key=lambda x: x.type)
        program_bicep.sort(key=lambda x: x.type)
        self.workouts["Arms"] = program_triceps + program_bicep

        leg_workout = WorkoutExercises(leg_exercises)
        program_legs = leg_workout.generate_exercises()
        shoulder_workout = WorkoutExercises(shoulder_exercises)
        program_shoulders = shoulder_workout.generate_exercises()
        program_legs.sort(key=lambda x: x.type)
        program_shoulders.sort(key=lambda x: x.type)
        self.workouts["Legs & Shoulders"] = program_legs + program_shoulders

    def generate_ppl_program(self):
        chest_workout = WorkoutExercises(chest_exercises)
        program_chest = chest_workout.generate_exercises()
        tricep_workout = WorkoutExercises(triceps_exercises)
        program_triceps = tricep_workout.generate_exercises()
        program_triceps.sort(key=lambda x: x.type)
        program_chest.sort(key=lambda x: x.type)
        self.workouts["Push"] = program_chest + program_triceps

        back_workout = WorkoutExercises(back_exercises)
        program_back = back_workout.generate_exercises()
        bicep_workout = WorkoutExercises(bicep_exercises)
        program_bicep = bicep_workout.generate_exercises()
        program_back.sort(key=lambda x: x.type)
        program_bicep.sort(key=lambda x: x.type)
        self.workouts["Pull"] = program_back + program_bicep

        leg_workout = WorkoutExercises(leg_exercises)
        program_legs = leg_workout.generate_exercises()
        shoulder_workout = WorkoutExercises(shoulder_exercises)
        program_shoulders = shoulder_workout.generate_exercises()
        program_legs.sort(key=lambda x: x.type)
        program_shoulders.sort(key=lambda x: x.type)
        self.workouts["Legs & Shoulders"] = program_legs + program_shoulders
    
    def generate_full_body_program(self):
        program_chest = WorkoutExercises(chest_exercises).generate_exercises()
        program_back = WorkoutExercises(back_exercises).generate_exercises()
        program_legs = WorkoutExercises(leg_exercises).generate_exercises()
        program_biceps = WorkoutExercises(bicep_exercises).generate_exercises()
        program_triceps = WorkoutExercises(triceps_exercises).generate_exercises()
        program_shoulders = WorkoutExercises(shoulder_exercises).generate_exercises()
        exercises_a = [program_chest[0], program_back[0], program_legs[0], program_biceps[0], program_triceps[0], program_shoulders[0]]
        self.workouts["Full Body A"] = exercises_a
        exercises_b = [program_chest[1], program_back[1], program_legs[1], program_biceps[1], program_triceps[1], program_shoulders[1]]
        self.workouts["Full Body B"] = exercises_b
        exercises_c = [program_chest[0], program_back[0], program_legs[0], program_biceps[2], program_triceps[2], program_shoulders[2]]
        self.workouts["Full Body C"] = exercises_c

    def print_program(self):
        for workout_name, exercises in self.workouts.items():
            print(f"{workout_name} Workout:")
            for exercise in exercises:
                exercise.print_exercise()
            print()

class Week:
    def __init__(self, program):
        self.program = program
        self.schedule = {}
    
    def generate_week_schedule(self):
        days = list(self.program.workouts.keys())
        for day in days:
            self.schedule[day] = self.program.workouts[day]

    def print_week_schedule(self):
        for day, exercises in self.schedule.items():
            print(f"{day}:")
            for exercise in exercises:
                exercise.print_exercise()
            print()

class TrainingBlock:
    def __init__(self, program, weeks=4):
        self.program = program
        self.weeks = []
        self.num_weeks = weeks

    def generate(self):
        for week_number in range(1, self.num_weeks + 1):
            self.program.generate_program()
            week = Week(self.program)
            week.generate_week_schedule()

            for day, exercises in week.schedule.items():
                week.schedule[day] = [copy.deepcopy(ex) for ex in exercises]

            for exercises in week.schedule.values():
                for ex in exercises:
                    ex.apply_progression(week_number)

            self.weeks.append(week)

full_body_program = WorkoutProgram(program_type=2)
workout_program = WorkoutProgram(program_type=1)
workout_program_arnold = WorkoutProgram(program_type=0)
block = TrainingBlock(workout_program, weeks=5)
block_arnold = TrainingBlock(workout_program_arnold, weeks=5)
block_full_body = TrainingBlock(full_body_program, weeks=5)
block.generate()
block_arnold.generate()
block_full_body.generate()

def export_block_to_light_pdf(block, filename="Training_Block.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    bg = HexColor("#FFFFFF")
    text = HexColor("#0F172A")
    accent = HexColor("#2563EB")
    muted = HexColor("#475569")

    for week_index, week in enumerate(block.weeks):
        c.setFillColor(bg)
        c.rect(0, 0, width, height, stroke=0, fill=1)

        y = height - 1.2 * inch

        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(text)
        c.drawString(1 * inch, y, f"Week {week_index + 1}")
        y -= 0.4 * inch

        for day, exercises in week.schedule.items():
            if y < 2 * inch:
                c.showPage()
                y = height - 1.2 * inch

            c.setFont("Helvetica-Bold", 17)
            c.setFillColor(accent)
            c.drawString(1 * inch, y, day)
            y -= 0.25 * inch

            c.setStrokeColor(accent)
            c.setLineWidth(1.2)
            c.line(1 * inch, y, width - 1 * inch, y)
            y -= 0.3 * inch

            for ex in exercises:
                c.setFont("Helvetica-Bold", 13)
                c.setFillColor(text)
                c.drawString(1.1 * inch, y, ex.name)

                c.setFont("Helvetica", 11)
                c.setFillColor(muted)
                c.drawRightString(
                    width - 1 * inch,
                    y,
                    f"{ex.sets} x {ex.reps}"
                )
                y -= 0.25 * inch

            y -= 0.35 * inch

        c.showPage()

    c.save()

export_block_to_light_pdf(block, filename="4_Week_PPL_Light.pdf")
export_block_to_light_pdf(block_arnold, filename="4_Week_ARNOLD_Light.pdf")
export_block_to_light_pdf(block_full_body, filename="4_Week_Full_Body_Light.pdf")