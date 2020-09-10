import subprocess
from collections import namedtuple

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

    def cget(self, control):
        cmd = f"amixer -c {self.card_id} -M cget iface=MIXER,name='{control}'"
        s = subprocess.run(cmd, shell=True, capture_output=True)

        if s.returncode != 0:
            # Throw exception!!!
            pass

        return self.__parse_amixer_stdout(s.stdout)
