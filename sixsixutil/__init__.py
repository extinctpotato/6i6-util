import alsaaudio, subprocess, logging, sys, time

logging.root.setLevel(logging.NOTSET)
l = logging.getLogger(__name__)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
l.addHandler(stream)
l.info("Test")

def get_card_id():
    cmd = 'aplay -l | grep "Scarlett 6i6" | cut -d " " -f 2 | tr -d ":"'
    s = subprocess.run(cmd, shell=True, capture_output=True)
    stdout = s.stdout.decode().strip('\n')
    card_id = None

    if len(stdout) > 0:
        try:
            card_id = int(stdout)
        except ValueError:
            pass

    return card_id

def amixer_cget(card_id, control):
    cmd = f"amixer -c {id} -M cget iface=MIXER,name='{control}'"
    s = subprocess.run(cmd, shell=True, capture_output=True)

    if s.returncode != 0:
        # Throw exception!!!
        pass

    spl = s.split("\n")


class SixAiSix:
    def __init__(self):
        self.id = get_card_id()
        self.controls = alsaaudio.mixers(self.id)

    def wiggle(self, schlafen=0):
        for c in self.controls:
            if c in ["Extension Unit", "Sample Clock Sync Status"]:
                continue

            mixer = alsaaudio.Mixer(cardindex=self.id, control=c)

            if len(mixer.getenum()) > 0:
                enums = mixer.getenum()

                current_sel = enums[0]
                current_sel_index = enums[1].index(current_sel)

                temp_sel_index = 0
                if current_sel == enums[1][temp_sel_index]:
                    temp_sel_index += 1

                l.info(f"{c}: {current_sel} <-> {enums[1][temp_sel_index]}")

                mixer.setenum(temp_sel_index)
                time.sleep(schlafen)
                mixer.setenum(current_sel_index)
            else:
                current_sel = mixer.getvolume()[0]

                if current_sel > 0:
                    temp_sel = current_sel-1
                else:
                    temp_sel = current_sel+1

                l.info(f"{c}: {current_sel} <-> {temp_sel}")

                mixer.setvolume(temp_sel)
                time.sleep(schlafen)
                mixer.setvolume(current_sel)
