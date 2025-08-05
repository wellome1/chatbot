from pluginBase import Plugin
import os
from dataclasses import dataclass; from typing import Optional

@dataclass
class Information:
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None

@dataclass
class Availabilities:
    Monday: Optional[list[str]] = None
    Tuesday: Optional[list[str]] = None
    Wednesday: Optional[list[str]] = None
    Thursday: Optional[list[str]] = None
    Friday: Optional[list[str]] = None
    Saturday: Optional[list[str]] = None
    Sunday: Optional[list[str]] = None

class ResumePlugin(Plugin):
    def __init__(self,
                 pluginName:str,
                 pluginDesc:str,
                 pluginTags:list[str],
                 triggerWords:list[str],
                 api,
                 function:callable=None,
                 overwrite:bool=False,
                 startBoot:bool=False
    ):
        if function is None: function = self.chooseCommand

        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite,
            startBoot=startBoot
        )

        self.experience = []
        self.skills = []
        self.education = []
        self.information = Information()
        self.availabilities = Availabilities()

    def chooseCommand(self, query=None):
        if query is None:
            print("Query expected!")
            return
        parts = query
        if parts is None:
            print("Invalid.")
            return

        if query == "export": self.export()
        splitList = parts[0].split()
        tempParts = [[splitList[0], splitList[1]]]
        for part in parts[1:]:
            tempParts.append(part)

        parts = tempParts

        match parts[0][0].lower():
            case "add":
                if parts[0][1] == "education":
                    self.addEducation(parts[1:])
                else:
                    self.addExperienceSkill(parts[1:], parts[0][1])
            case "information":
                self.addInformation(parts[1:], parts[0][1])
            case "availability":
                self.addAvailability(parts[1:], parts[0][1])

            case _:
                print(f"Invalid query. Unknown command: \'{parts[0][0]} {parts[0][1]}\'.")
                return

    def addExperienceSkill(self, queryParts:list, experienceSkill:str):
        if not experienceSkill:
            print("Please specify what you want me to add (experience/skill).")
            return

        if experienceSkill.lower() not in ("experience", "skill"):
            print("Invalid option. Please specify between experience/skill.")
            return

        if len(queryParts) != 4 and experienceSkill.lower() == "experience":
            print("Missing some data. Note: You can add 4 fields, separated by \"|\".")
        if len(queryParts[1:]) != 4 and experienceSkill.lower() == "skill":
            print("Missing some data. Note: You can add 3 fields, separated by \"|\".")

        if experienceSkill.lower() == "experience":
            position = queryParts[0] if len(queryParts) >= 1 else ""
            company = queryParts[1] if len(queryParts) >= 2 else ""
            duration = queryParts[2] if len(queryParts) >= 3 else ""
            description = queryParts[3] if len(queryParts) >= 4 else ""
            self.experience.append([position, company, duration, description])
            print(f"Experience added.\nPosition: {position}\nCompany: {company}\nDuration: {duration}\nDescription: {description}")
            return

        elif experienceSkill.lower() == "skill":
            skillName = queryParts[0] if queryParts[0] else ""
            durationPracticed = queryParts[1] if queryParts[1] else ""
            description = queryParts[2] if queryParts[2] else ""
            self.skills.append([skillName, durationPracticed, description])
            print(f"Skill added.\nSkill name: {skillName}\nDuration practiced: {durationPracticed}\nDescription: {description}.")
            return

    def addInformation(self, queryParts, infoToAdd):
        if not queryParts or not infoToAdd:
            print("Please specify what you want me to add (name/address/phone/email/birthday).")
            return
        if infoToAdd.lower() not in ("name", "address", "phone", "email", "birthday"):
            print("Invalid option. Please specify between name/address/phone/email/birthday.")
            return

        match infoToAdd.lower():
            case "name":
                self.information.name = ' '.join(queryParts)
                print(f"Added name to information: {self.information.name}.")
                return
            case "address":
                self.information.address = ' '.join(queryParts)
                print(f"Added address to information: {self.information.address}.")
                return
            case "phone":
                self.information.phone = ' '.join(queryParts)
                print(f"Added phone to information: {self.information.phone}.")
                return
            case "email":
                self.information.email = ' '.join(queryParts)
                print(f"Added email to information: {self.information.email}.")
                return
            case "birthday":
                self.information.birthday = ' '.join(queryParts)
                print(f"Added birthday to information: {self.information.birthday}.")
                return

            case _:
                print("How the hell did you get here? I checked you before!")
                print(f"Remember this to let me know: {infoToAdd}.")
                return

    def addAvailability(self, queryParts, day:str):
        if not queryParts or not day:
            print("Please specify what you want me to add (day & time frames, connect times with a '-').")
            return
        if day.lower() not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            print("Please choose a day!")
            return

        day = day.capitalize()

        for part in queryParts:
            part = str(part)
            value = getattr(self.availabilities, day)
            if value is None:
                setattr(self.availabilities, day, [part])
            else:
                value.append(part)

            print(f"Added availability for {day}: {part}.")

    def addEducation(self, queryParts):
        if not queryParts:
            print("Please specify what you want me to add (education).")
            return

        institution = queryParts[0]
        duration = ' '.join(queryParts[1:])

        self.education.append([institution, duration])
        print(f"Added education for {institution}: {duration}.")

    def export(self, outputPath=None):
        if outputPath is None:
            outputPath = os.path.join(os.getcwd(), "resume.md")

        for field in ["name", "address", "phone", "email", "birthday"]:
            if getattr(self.information, field) is None:
                setattr(self.information, field, "")
                print(f"Warning! {field} is missing. Will be put as blank...")


        for field in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            field = field.capitalize()
            if getattr(self.availabilities, field) is None:
                setattr(self.availabilities, field, ["Unavailable"])
                print(f"{field} has no availabilities. Will be put as unavailable...")

        if len(self.experience) == 0:
                print(f"Experience is empty. Will be left empty...")

        if len(self.skills) == 0:
            print(f"Skill is empty. Will be left empty...")

        print("Creating resume now...")

        lines = [
            # Information
            f"# Resume - {self.information.name}",
            f"- Address: {self.information.address}",
            f"- Phone No.: {self.information.phone}",
            f"- Email Address: {self.information.email}",
            f"- Birthday: {self.information.birthday}",
            f"{'-'*40}\n",
            f"## Education"
        ]

        # Education
        for education in self.education:
            lines.append(f"- {education[0]}: {education[1]}")

        lines.append(f"\n{'-'*40}\n")

        # Experience
        lines.append(f"## Experience")
        for experience in self.experience:
            lines.append(f"- {experience[0]}")
            lines.append(f"{experience[1]}\n{experience[2]}\n{experience[3]}\n")

        lines.append(f"\n{'-'*40}\n")

        # Skills
        lines.append(f"\n## Skills")
        for skill in self.skills:
            lines.append(f"- {skill[0]}")
            lines.append(f"{skill[1]}\n{skill[2]}\n")

        lines.append(f"\n{'-'*40}\n")

        # Availabilities
        lines.append(f"## Availability")
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            day = day.capitalize()
            times = getattr(self.availabilities, day)
            lines.append(f"- {day}: {' '.join(times)}")

        # Writing to file
        print("Writing resume to file...")

        with open(outputPath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Done! You can find resume at: {outputPath}.")

