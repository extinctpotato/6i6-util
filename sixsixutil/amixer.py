import subprocess
from collections import namedtuple

class AmixerException(Exception):
    def __init__(self, message):
        self.message = message.replace("\n", "")
        super().__init__(self.message)

class ControlNotFound(AmixerException):
    pass

class CardNotFound(AmixerException):
    pass

class Amixer:
    def __init__(self, card_id):
        self.card_id = card_id

    def __parse_amixer_stdout(self, stdout_bytes):
        d = {}
        spl = stdout_bytes.decode().split("\n")

        while "" in spl:
            spl.remove("")

        d["vol"] = [int(vol) for vol in spl[2].split("=")[1].split(",")]
        del spl[2]

        for el in spl:
            for values in el.split(","):
                key_val = values.split("=")
                key = key_val[0].replace(" ", "") \
                                .replace("|", "") \
                                .replace(";", "") \
                                .replace("-", "_") \
                                .lower()
                while key in d.keys():
                    key = key+"_alt"

                try:
                    val = int(key_val[1])
                except ValueError:
                    val = key_val[1]

                d[key] = val

        return namedtuple("AmixerResult", d.keys())(*d.values())

    def __run_amixer(self, params):
        cmd = f"amixer {params}"
        s = subprocess.run(cmd, shell=True, capture_output=True)

        if s.returncode != 0:
            stderr = s.stderr.decode()
            if "Cannot find the given element from control" in stderr:
                raise ControlNotFound(stderr)
            elif "Invalid card number" in stderr:
                raise CardNotFound(stderr)

        return self.__parse_amixer_stdout(s.stdout)

    def cget(self, control):
        cmd = f"-c {self.card_id} -M cget iface=MIXER,name='{control}'"
        return self.__run_amixer(cmd)

    def cset(self, control, left, right):
        cmd = f"-c {self.card_id} cset iface=MIXER,name='{control}' {left},{right}"
        return self.__run_amixer(cmd)
