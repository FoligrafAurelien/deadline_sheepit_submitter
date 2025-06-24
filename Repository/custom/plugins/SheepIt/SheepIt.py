from Deadline.Plugins import DeadlinePlugin, PluginType
import sys
import os

def GetDeadlinePlugin():
    return SheepItPlugin()

def CleanupDeadlinePlugin(deadlinePlugin):
    deadlinePlugin.Cleanup()

class SheepItPlugin(DeadlinePlugin):
    def __init__(self):
        # Appel natif pour héritage Python 2/3, pattern validé dans TOUS les plugins
        if sys.version_info.major == 3:
            super().__init__()
        else:
            super(SheepItPlugin, self).__init__()

        # Enregistrement des callbacks natifs Deadline
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        self.StartJobCallback += self.StartJob
        self.EndJobCallback += self.EndJob

        # Si tu as besoin de RenderTasksCallback, rajoute-le ici
        # self.RenderTasksCallback += self.RenderTasks

        self.process = None

    def Cleanup(self):
        self.LogInfo("Cleaning up SheepIt plugin.")
        # Si tu as un process SheepIt lancé, tu le termines ici
        if self.process and self.process.poll() is None:
            self.LogInfo("Terminating SheepIt process.")
            self.process.terminate()

    def InitializeProcess(self):
        self.LogInfo("Initializing SheepIt process.")
        self.SingleFramesOnly = True
        self.PluginType = PluginType.Simple

    def RenderExecutable(self):
        plugin_dir = self.GetPluginDirectory()
        java_path = os.path.join(plugin_dir, "client", "java", "bin", "java.exe")
        return java_path

    def RenderArgument(self):
        # Chemin du .jar SheepIt
        plugin_dir = self.GetPluginDirectory()
        jar_path = os.path.join(plugin_dir, "client", "sheepit-client.jar")

        login = self.GetPluginInfoEntry("Login")
        password = self.GetPluginInfoEntry("Password")
        systotrail = self.GetBooleanPluginInfoEntryWithDefault("Systotrail", False)

        args = [
            "-jar", jar_path,
            "-ui", "text",
            "-login", login,
            "-password", password
        ]
        if systotrail:
            args.append("--systotrail")

        return " ".join('"{}"'.format(a) if ' ' in a else str(a) for a in args)

    def StartJob(self):
        self.LogInfo("SheepIt job is starting.")

    def EndJob(self):
        self.LogInfo("SheepIt job is ending.")

    # Exemple d'extension : callback RenderTasks si tu veux un contrôle avancé (optionnel)
    # def RenderTasks(self):
    #     # Logique custom ici

