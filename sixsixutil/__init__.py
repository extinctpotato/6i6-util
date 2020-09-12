import alsaaudio, subprocess, logging, sys, time
from sixsixutil import amixer
from collections import namedtuple

l = logging.getLogger(__name__)

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

class SixAiSix:
    def __init__(self):
        self.id = get_card_id()
        self.controls = alsaaudio.mixers(self.id)
        self.amixer = amixer.Amixer(self.id)

    def wiggle(self, schlafen=0, use_amixer=True):
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
            elif not use_amixer:
                current_sel = mixer.getvolume()[0]

                if current_sel > 0:
                    temp_sel = current_sel-1
                else:
                    temp_sel = current_sel+1

                l.info(f"{c}: {current_sel} <-> {temp_sel}")

                mixer.setvolume(temp_sel)
                time.sleep(schlafen)
                mixer.setvolume(current_sel)
            elif use_amixer:
                amixer_name = f"{c} Playback Volume"
                current_sel = self.amixer.cget(amixer_name).vol
                if len(current_sel) == 1:
                    current_sel.append(current_sel[0])
                temp_sel = [el for el in current_sel]

                for i in range(0, len(temp_sel)):
                    if temp_sel[i] > 0:
                        temp_sel[i] -= 1
                    else:
                        temp_sel[i] += 1

                l.info(f"{c}: {current_sel} <-> {temp_sel}")

                self.amixer.cset(amixer_name, temp_sel[0], temp_sel[1])
                time.sleep(schlafen)
                self.amixer.cset(amixer_name, current_sel[0], current_sel[1])
