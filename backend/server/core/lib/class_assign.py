class Timetable:
    """
    period_count: number of periods in total
    student_classes: [student1's classes: [high priority -> low priority], student2's classes, ...]
     -> Remember to put at most just as many classes as there are periods, or the system will not work.
    teacher_classes: [classes teacher1 teaches: [classes], classes teacher2 teaches, ...]
    """

    def __init__(self, period_count: int, student_classes: list, teacher_classes: list, student_name_dict: list, teacher_name_dict: list, class_caps: dict):
        self.periods = [[] for _ in range(period_count)]
        self.teacher_classes = teacher_classes
        self.student_name_dict = []
        self.teacher_name_dict = teacher_name_dict
        self.class_caps = class_caps
        for i in range(len(student_classes)):  # each student by ID
            self.add_student(student_classes[i], student_name_dict[i])

    def get_student_classes(self, id_num: int):
        """Gets all the periods of the student from their ID in order."""

        ret = []
        for i in self.periods:
            ret.append(i[id_num])
        return ret

    def get_teacher_classes(self, id_num: int):
        """Gets all the periods of the teacher from their ID in order."""

        ret = []
        for i in self.periods:
            current_class = None
            for p in i:  # each student's class
                if p in self.teacher_classes[id_num]:
                    current_class = p
                    break
            ret.append(current_class)
        return ret

    def add_student_class(self, id_num, class_name):
        """Adds a class to a student's timetable, where it will fit."""

        cap_not_exceeded = -2
        for li in range(len(self.periods)):  # each period [st1-cl1, st2-None, ...]
            l = self.periods[li]
            for m in l:  # each student's class
                if cap_not_exceeded == -2:
                    cap_not_exceeded = -1
                class_counts = {}
                for m in l + [class_name]:
                    if m not in class_counts:
                        class_counts[m] = 0
                    class_counts[m] += 1
                add = True
                if l[id_num]:
                    add = False
                if class_name in self.class_caps.keys():
                    if class_counts[class_name] > self.class_caps[class_name]:
                        add = False
                if add:
                    if cap_not_exceeded == -1:
                        cap_not_exceeded = li
                if m == class_name and not l[id_num] and add:
                    if cap_not_exceeded == -1:
                        cap_not_exceeded = li
                    l[id_num] = class_name
                    return
        added = False
        if cap_not_exceeded != -1:
            for li in range(max(0, cap_not_exceeded), len(self.periods)):  # each period [st1-cl1, st2-None, ...]
                l = self.periods[li]
                if not l[id_num]:
                    overlap = False
                    for m in range(len(self.teacher_classes)):  # each teacher by ID
                        this_teacher_classes = []
                        for n in l + [class_name]:  # each student's class
                            if n in self.teacher_classes[m]:
                                if n not in this_teacher_classes:
                                    this_teacher_classes.append(n)
                                if len(this_teacher_classes) > 1:
                                    overlap = True
                                    break
                        if overlap:
                            break
                    if not overlap:
                        l[id_num] = class_name
                        added = True
                        break
        if not added or cap_not_exceeded == -1:
            print("\033[31mError in agenda -> Errno 1\n\tStudent with ID " + str(id_num) + " and name " + self.student_name_dict[id_num] + " missing class " + class_name + ".\n\tCurrent agenda of student: " + str(self.get_student_classes(id_num)) + ".\033[0m")
            return

    def modify_student_class(self, id_num: int, period_index: int, new_class_name=None):
        """Changes the class of a student during a period. Defaults to removing the class."""

        self.periods[period_index][id_num] = new_class_name

    def add_student(self, class_names: list, student_name: str):
        """Adds a new student with a new ID."""

        id_num = len(self.periods[0])
        self.student_name_dict.append(student_name)
        for p in self.periods:
            p.append(None)
        for p in class_names:  # each class
            self.add_student_class(id_num, p)
        return id_num

    def add_teacher(self, class_names: list, teacher_name: str):
        """Adds a new student with a new ID."""

        id_num = len(self.teacher_classes)
        self.teacher_name_dict.append(teacher_name)
        self.teacher_classes.append(class_names)
        return id_num

    def remove_student(self, name):
        """Removes a student from the database."""

        for i in range(len(self.student_name_dict)):
            if self.student_name_dict[i] == name:
                self.remove_student_id(i)
                break

    def remove_student_id(self, id_num):
        self.student_name_dict[id_num] = "(removed student) " + student_name_dict[id_num]
        for i in self.periods:
            i[id_num] = None

    def remove_teacher(self, name):
        """Adds a new student with a new ID."""

        for i in range(len(self.teacher_name_dict)):
            if self.teacher_name_dict[i] == name:
                self.remove_teacher_id(i)
                break

    def remove_teacher_id(self, id_num):
        self.teacher_name_dict[id_num] = "(removed teacher) " + teacher_name_dict[id_num]
        self.teacher_classes[id_num] = []


if __name__ == "__main__":
    student_name_dict = ["Mike", "Tom", "Bob"]  # The names of the students, from their IDs
    teacher_name_dict = ["Mr. B", "Ms. W"]  # The names of the teachers, from their IDs
    class_caps = {"Mathematics": 3, "English (HL)": 2}
    student_classes = [["Mathematics", "English (SL)", "PST"], ["Mathematics", "English (HL)", "PST"], ["Mathematics", "English (HL)", "SPST"]]
    timetable = Timetable(3, student_classes, [["English (SL)", "English (HL)"], ["Mathematics"]], student_name_dict, teacher_name_dict, class_caps)
    for i in range(len(teacher_name_dict)):
        print("(Teacher) Classes of " + timetable.teacher_name_dict[i] + ":", timetable.get_teacher_classes(i))
    print()
    for i in range(len(student_name_dict)):
        print("(Student) Classes of " + timetable.student_name_dict[i] + ":", timetable.get_student_classes(i))
