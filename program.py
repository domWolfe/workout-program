import copy
import random

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QHeaderView, QComboBox, QHBoxLayout,
    QDialog, QListWidget, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

import json

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
        if adjusted_week == 3:
            self.sets = min(self.base_sets + 1, 4)
            low, high = map(int, self.base_reps.split("-"))
            self.reps = f"{low+1}-{high+1}"
        elif adjusted_week > 3 and adjusted_week <= 4:
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

    def remove_exercise(self, name):
        self.exercises = [e for e in self.exercises if e.name != name]

    def get_exercises_by_type(self, type) -> list:
        return [exercise for exercise in self.exercises if exercise.type == type]

    def to_dict(self):
        return [
            {"name": e.name, "type": e.type, "link": e.link}
            for e in self.exercises
        ]

    def load_from_dict(self, data):
        self.exercises.clear()
        for e in data:
            self.add_exercise_by_con(e["name"], e["type"], e.get("link", ""))

    
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

EXERCISE_POOLS = {
    "Chest": chest_exercises,
    "Triceps": triceps_exercises,
    "Back": back_exercises,
    "Biceps": bicep_exercises,
    "Legs": leg_exercises,
    "Shoulders": shoulder_exercises
}

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
block_full_body = TrainingBlock(full_body_program, weeks=10)
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
        if (week_index + 1) % 5 == 0:  
            c.drawString(1 * inch, y, f"Week {week_index + 1} (Heavy)")
        else:
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

def export_nutrition_to_light_pdf(
    weight_kg,
    height_cm,
    age,
    sex,
    activity_label,
    activity_factor,
    filename="Nutrition_Plan.pdf"
    ):
    maintenance = NutritionCalculator.maintenance_calories(
        weight_kg, height_cm, age, sex, activity_factor
    )
    bulk = NutritionCalculator.bulk_calories(maintenance)
    cut = NutritionCalculator.cut_calories(maintenance)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    bg = HexColor("#FFFFFF")
    text = HexColor("#0F172A")
    accent = HexColor("#2563EB")
    muted = HexColor("#475569")

    c.setFillColor(bg)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    y = height - 1.2 * inch

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(text)
    c.drawString(1 * inch, y, "Nutrition Overview")
    y -= 0.5 * inch

    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(1 * inch, y, width - 1 * inch, y)
    y -= 0.6 * inch

    # Stats
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(accent)
    c.drawString(1 * inch, y, "Client Stats")
    y -= 0.35 * inch

    c.setFont("Helvetica", 13)
    c.setFillColor(text)
    stats = [
        f"Weight: {weight_kg} kg",
        f"Height: {height_cm} cm",
        f"Age: {age}",
        f"Sex: {sex}",
        f"Activity Level: {activity_label}"
    ]

    for s in stats:
        c.drawString(1.1 * inch, y, s)
        y -= 0.25 * inch

    y -= 0.4 * inch

    # Calories
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(accent)
    c.drawString(1 * inch, y, "Daily Calories")
    y -= 0.35 * inch

    c.setFont("Helvetica", 14)
    c.setFillColor(text)

    c.drawString(1.1 * inch, y, f"Maintenance Calories:")
    c.drawRightString(width - 1 * inch, y, f"{maintenance} kcal")
    y -= 0.3 * inch

    c.drawString(1.1 * inch, y, f"Lean Bulk Calories:")
    c.drawRightString(width - 1 * inch, y, f"{bulk} kcal")
    y -= 0.3 * inch

    c.drawString(1.1 * inch, y, f"Fat Loss Calories:")
    c.drawRightString(width - 1 * inch, y, f"{cut} kcal")
    y -= 0.6 * inch

    c.save()


export_block_to_light_pdf(block, filename="4_Week_PPL_Light.pdf")
export_block_to_light_pdf(block_arnold, filename="4_Week_ARNOLD_Light.pdf")
export_block_to_light_pdf(block_full_body, filename="4_Week_Full_Body_Light.pdf")

class ProgramGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workout Program Generator & Multi-Week Preview")
        self.setGeometry(100, 100, 800, 500)

        self.training_block = None
        self.week_number = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        top_layout = QHBoxLayout()
        self.layout.addLayout(top_layout)

        top_layout.addWidget(QLabel("Program Type:"))
        self.program_selector = QComboBox()
        self.program_selector.addItems(["PPL", "Arnold Split", "Full Body"])
        top_layout.addWidget(self.program_selector)

        self.generate_button = QPushButton("Generate Program")
        self.generate_button.clicked.connect(self.generate_program)
        top_layout.addWidget(self.generate_button)

        self.week_label = QLabel("")
        self.week_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.week_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Day", "Exercise", "Type", "Sets", "Reps"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        nav_layout = QHBoxLayout()
        self.layout.addLayout(nav_layout)

        self.prev_week_btn = QPushButton("<< Previous Week")
        self.prev_week_btn.clicked.connect(self.prev_week)
        nav_layout.addWidget(self.prev_week_btn)

        self.next_week_btn = QPushButton("Next Week >>")
        self.next_week_btn.clicked.connect(self.next_week)
        nav_layout.addWidget(self.next_week_btn)

        self.save_btn = QPushButton("Save Current Week Edits")
        self.save_btn.clicked.connect(self.save_week)
        nav_layout.addWidget(self.save_btn)

        self.nutrition_btn = QPushButton("Nutrition Calculator")
        self.nutrition_btn.clicked.connect(self.open_nutrition)
        nav_layout.addWidget(self.nutrition_btn)

        self.manage_btn = QPushButton("Manage Exercises")
        self.manage_btn.clicked.connect(self.open_exercise_manager)
        nav_layout.addWidget(self.manage_btn)

        self.export_ex_btn = QPushButton("Export Exercises")
        self.export_ex_btn.clicked.connect(lambda: export_exercises_to_json())
        nav_layout.addWidget(self.export_ex_btn)

        self.import_ex_btn = QPushButton("Import Exercises")
        self.import_ex_btn.clicked.connect(self.import_exercises)
        nav_layout.addWidget(self.import_ex_btn)

        self.save_pdf_btn = QPushButton("Export Training Block to PDF")
        self.save_pdf_btn.clicked.connect(self.save_week)
        self.save_pdf_btn.clicked.connect(self.export_current_block_to_pdf)
        nav_layout.addWidget(self.save_pdf_btn)

    def export_current_block_to_pdf(self):
        if self.training_block:
            filename = f"Training_Block_Week_{len(self.training_block.weeks)}.pdf"
            export_block_to_light_pdf(self.training_block, filename=filename)
            print(f"Exported current training block to {filename}")

    def open_exercise_manager(self):
        dlg = ExerciseManager(self)
        dlg.exec()

    def import_exercises(self):
        import_exercises_from_json()
        print("Exercise config imported.")

    def open_nutrition(self):
        dlg = NutritionDialog(self)
        dlg.exec()

    def generate_program(self):
        program_type = self.program_selector.currentText()
        if program_type == "PPL":
            wp = WorkoutProgram(program_type=1)
        elif program_type == "Arnold Split":
            wp = WorkoutProgram(program_type=0)
        else:
            wp = WorkoutProgram(program_type=2)
        
        self.training_block = TrainingBlock(wp, weeks=5)
        self.training_block.generate()
        self.week_number = 0
        self.show_week()

    def show_week(self):
        week = self.training_block.weeks[self.week_number]
        self.week_label.setText(f"Week {self.week_number + 1}")

        # Count total exercises
        total_exercises = sum(len(exs) for exs in week.schedule.values())
        self.table.setRowCount(total_exercises)

        row_index = 0
        for day, exercises in week.schedule.items():
            for ex in exercises:
                self.table.setItem(row_index, 0, QTableWidgetItem(day))
                self.table.item(row_index, 0).setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row_index, 1, QTableWidgetItem(ex.name))
                self.table.item(row_index, 1).setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row_index, 2, QTableWidgetItem(str(ex.type)))
                self.table.item(row_index, 2).setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row_index, 3, QTableWidgetItem(str(ex.sets)))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(ex.reps)))
                row_index += 1

    def save_week(self):
        week = self.training_block.weeks[self.week_number]
        row_index = 0
        for day, exercises in week.schedule.items():
            for i, ex in enumerate(exercises):
                sets = self.table.item(row_index, 3).text()
                reps = self.table.item(row_index, 4).text()
                ex.sets = int(sets)
                ex.reps = reps
                row_index += 1
        print(f"Week {self.week_number + 1} edits saved.")

    def next_week(self):
        if self.training_block and self.week_number < len(self.training_block.weeks) - 1:
            self.save_week()
            self.week_number += 1
            self.show_week()

    def prev_week(self):
        if self.training_block and self.week_number > 0:
            self.save_week()
            self.week_number -= 1
            self.show_week()

class ExerciseManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exercise Manager")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        self.group_selector = QComboBox()
        self.group_selector.addItems(EXERCISE_POOLS.keys())
        self.group_selector.currentTextChanged.connect(self.refresh_list)
        layout.addWidget(self.group_selector)

        self.exercise_list = QListWidget()
        layout.addWidget(self.exercise_list)

        form = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Exercise Name")
        self.type_input = QComboBox()
        self.type_input.addItems(["0", "1", "2", "3"])
        form.addWidget(self.name_input)
        form.addWidget(self.type_input)
        layout.addLayout(form)

        btns = QHBoxLayout()
        add_btn = QPushButton("Add")
        remove_btn = QPushButton("Remove Selected")
        add_btn.clicked.connect(self.add_exercise)
        remove_btn.clicked.connect(self.remove_exercise)
        btns.addWidget(add_btn)
        btns.addWidget(remove_btn)
        layout.addLayout(btns)

        self.refresh_list()

    def current_pool(self):
        return EXERCISE_POOLS[self.group_selector.currentText()]

    def refresh_list(self):
        self.exercise_list.clear()
        for e in self.current_pool().exercises:
            self.exercise_list.addItem(f"{e.name} (Type {e.type})")

    def add_exercise(self):
        name = self.name_input.text().strip()
        if not name:
            return
        self.current_pool().add_exercise_by_con(
            name, int(self.type_input.currentText())
        )
        self.name_input.clear()
        self.refresh_list()

    def remove_exercise(self):
        item = self.exercise_list.currentItem()
        if not item:
            return
        name = item.text().split(" (")[0]
        self.current_pool().remove_exercise(name)
        self.refresh_list()

def export_exercises_to_json(filename="exercise_config.json"):
    data = {k: v.to_dict() for k, v in EXERCISE_POOLS.items()}
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def import_exercises_from_json(filename="exercise_config.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    for group, exercises in data.items():
        if group in EXERCISE_POOLS:
            EXERCISE_POOLS[group].load_from_dict(exercises)

class NutritionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nutrition Calculator")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        self.weight = QLineEdit()
        self.weight.setPlaceholderText("Weight (kg)")

        self.height = QLineEdit()
        self.height.setPlaceholderText("Height (cm)")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")

        self.sex = QComboBox()
        self.sex.addItems(["Male", "Female"])

        self.activity = QComboBox()
        self.activity_levels = {
            "Sedentary (1.2)": 1.2,
            "Light (1.375)": 1.375,
            "Moderate (1.55)": 1.55,
            "Very Active (1.725)": 1.725,
        }
        self.activity.addItems(self.activity_levels.keys())

        self.result = QLabel("")
        self.result.setAlignment(Qt.AlignCenter)

        calc_btn = QPushButton("Calculate Calories")
        export_btn = QPushButton("Export Nutrition PDF")

        calc_btn.clicked.connect(self.calculate)
        export_btn.clicked.connect(self.export_pdf)

        for w in [self.weight, self.height, self.age, self.sex, self.activity]:
            layout.addWidget(w)

        layout.addWidget(calc_btn)
        layout.addWidget(export_btn)
        layout.addWidget(self.result)

    def export_pdf(self):
        try:
            weight = float(self.weight.text())
            height = float(self.height.text())
            age = int(self.age.text())
            sex = self.sex.currentText()
            activity_label = self.activity.currentText()
            activity_factor = self.activity_levels[activity_label]

            filename = "Nutrition_Plan_Light.pdf"

            export_nutrition_to_light_pdf(
                weight, height, age, sex,
                activity_label, activity_factor,
                filename=filename
            )

            QMessageBox.information(
                self,
                "Export Successful",
                f"Nutrition plan exported to {filename}"
            )
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please calculate first.")

    def calculate(self):
        try:
            maintenance = NutritionCalculator.maintenance_calories(
                weight_kg=float(self.weight.text()),
                height_cm=float(self.height.text()),
                age=int(self.age.text()),
                sex=self.sex.currentText(),
                activity_factor=self.activity_levels[self.activity.currentText()]
            )

            bulk = NutritionCalculator.bulk_calories(maintenance)
            cut = NutritionCalculator.cut_calories(maintenance)

            self.result.setText(
                f"Maintenance: {maintenance} kcal\n"
                f"Lean Bulk: {bulk} kcal\n"
                f"Fat Loss: {cut} kcal"
            )
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")


class NutritionCalculator:
    @staticmethod
    def maintenance_calories(weight_kg, height_cm, age, sex, activity_factor):
        if sex.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        return int(bmr * activity_factor)

    @staticmethod
    def bulk_calories(maintenance, surplus_pct=0.10):
        return int(maintenance * (1 + surplus_pct))

    @staticmethod
    def cut_calories(maintenance, deficit_pct=0.20):
        return int(maintenance * (1 - deficit_pct))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ProgramGUI()
    gui.show()
    sys.exit(app.exec())