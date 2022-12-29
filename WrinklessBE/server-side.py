import subprocess

class ScriptRunner:
    def __init__(self, filename):
        self.filename = filename
        self.output = None
        self.error = None

    def call_script(self):
        process = subprocess.Popen(['python', self.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        self.output, self.error = process.communicate()

        if self.error != None:
            raise Exception(self.error.decode("utf-8"))
        self.output = self.output.decode("utf-8")

        return self.output

    def stop_script(self):
        process = subprocess.Popen(['python', self.filename])
        try:
            process.terminate()
        except Exception as e:
            # process.kill()
            raise Exception(f"Error! Tratando de terminar el progrma. Inner exception {e}")
