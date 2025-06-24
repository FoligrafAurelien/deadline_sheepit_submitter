# SubmitSheepItJob.py - Official pattern, Deadline 10.3, with Whitelist/MachineListBox and sticky settings

from Deadline.Scripting import ClientUtils
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog
from System.IO import Path, StreamWriter
from System.Text import Encoding

scriptDialog = None

def GetSettingsFilename():
    return Path.Combine(ClientUtils.GetUsersSettingsDirectory(), "SheepItSettings.ini")

def __main__():
    global scriptDialog
    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle("Submit SheepIt Job")

    # ===== Job Description =====
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator1", "SeparatorControl", "Job Description", 0, 0, colSpan=2)
    scriptDialog.AddControlToGrid("NameLabel", "LabelControl", "Job Name", 1, 0)
    scriptDialog.AddControlToGrid("NameBox", "TextControl", "SheepIt Job", 1, 1)
    scriptDialog.EndGrid()

    # ===== Workstations =====
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator2", "SeparatorControl", "Workstations", 0, 0, colSpan=2)
    scriptDialog.AddControlToGrid("MachineListLabel", "LabelControl", "Machine List", 1, 0)
    scriptDialog.AddControlToGrid("MachineListBox", "MachineListControl", "", 1, 1, colSpan=2)
    scriptDialog.EndGrid()

    # ===== SheepIt Options =====
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator3", "SeparatorControl", "SheepIt Options", 0, 0, colSpan=2)
    scriptDialog.AddControlToGrid("LoginLabel", "LabelControl", "Login", 1, 0)
    scriptDialog.AddControlToGrid("LoginBox", "TextControl", "", 1, 1)
    scriptDialog.AddControlToGrid("PasswordLabel", "LabelControl", "Password", 2, 0)
    scriptDialog.AddControlToGrid("PasswordBox", "PasswordControl", "", 2, 1)
    scriptDialog.AddControlToGrid("SystotrailLabel", "LabelControl", "Enable Systotrail", 3, 0)
    scriptDialog.AddControlToGrid("SystotrailBox", "CheckBoxControl", False, 3, 1)
    scriptDialog.AddControlToGrid("MachineCountLabel", "LabelControl", "Number of Machines", 4, 0)
    scriptDialog.AddControlToGrid("MachineCountBox", "TextControl", "1", 4, 1)
    scriptDialog.EndGrid()

    scriptDialog.AddControl("Separator", "SeparatorControl", "")
    submitButton = scriptDialog.AddControl("SubmitButton", "ButtonControl", "Submit")
    closeButton = scriptDialog.AddControl("CloseButton", "ButtonControl", "Close")

    closeButton.ValueModified.connect(scriptDialog.closeEvent)
    submitButton.ValueModified.connect(SubmitButtonPressed)

    # Native pattern: sticky settings for MachineListBox, etc.
    settings = ("MachineListBox",)
    scriptDialog.LoadSettings(GetSettingsFilename(), settings)
    scriptDialog.EnabledStickySaving(settings, GetSettingsFilename())

    scriptDialog.ShowDialog()

def SubmitButtonPressed(*args):
    global scriptDialog

    jobName = scriptDialog.GetValue("NameBox").strip() or "SheepIt Job"
    login = scriptDialog.GetValue("LoginBox").strip()
    password = scriptDialog.GetValue("PasswordBox")
    systotrail = scriptDialog.GetValue("SystotrailBox")
    machineCount = scriptDialog.GetValue("MachineCountBox").strip()
    machineList = scriptDialog.GetValue("MachineListBox").strip()

    try:
        machineCountInt = int(machineCount)
        if machineCountInt < 1:
            raise ValueError
    except:
        scriptDialog.ShowMessageBox("Number of Machines must be a positive integer.", "Error")
        return

    # ===== Write job info file =====
    jobInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "sheepit_job_info.job")
    writer = StreamWriter(jobInfoFilename, False, Encoding.Unicode)
    writer.WriteLine("Plugin=SheepIt")
    writer.WriteLine("Name=%s" % jobName)
    writer.WriteLine("Frames=0-%d" % (machineCountInt-1))
    # Only Whitelist, never MachineList nor SingleFramesOnly
    if machineList:
        writer.WriteLine("Whitelist=%s" % machineList)
    writer.Close()

    # ===== Write plugin info file =====
    pluginInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "sheepit_plugin_info.job")
    writer = StreamWriter(pluginInfoFilename, False, Encoding.Unicode)
    writer.WriteLine("Login=%s" % login)
    writer.WriteLine("Password=%s" % password)
    writer.WriteLine("Systotrail=%s" % str(systotrail))
    writer.Close()

    # ===== Submit to Deadline =====
    arguments = [jobInfoFilename, pluginInfoFilename]
    results = ClientUtils.ExecuteCommandAndGetOutput(arguments)
    scriptDialog.ShowMessageBox(results, "Submission Results")

