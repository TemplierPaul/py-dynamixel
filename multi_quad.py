from quadruped_controller import Quadruped
import time
import py_dynamixel.io as io


class MultiQuad:
    def __init__(self, ports, ctrl_freq):
        print("Ports", ports)
        self.QTs = [
            Quadruped(ports[i], ctrl_freq) for i in range(len(ports))
        ]
        self.ctrl_freq = ctrl_freq
        self.ports = ports


    def _exec_step(self):
        for QT in self.QTs:
            QT._exec_step()

    def neutral_controller(self):
        for QT in self.QTs:
            print(f"Neutral controller for QT {QT.port}")
            QT.neutral_controller()

    def run_new_sin_controller(self, ctrl, duration=4.0):
        for QT in self.QTs:
            QT.run_new_sin_controller(ctrl, duration)

    def shutdown(self):
        for QT in self.QTs:
            QT.shutdown()

    def _exec_traj(self):
        start = time.time()
        traj_len = max(len(QT._traj) for QT in self.QTs)
        for _ in range(traj_len):
            # get current state
            #cur_jpos = self.dxl_io.get_present_position(self.ids)
            #cur_jvel = self.dxl_io.get_present_velocity(self.ids)
            #print(cur_jpos, cur_jvel)

            # get action
            self._exec_step()
            elapsed = time.time() - start
            time.sleep((1.0/self.ctrl_freq) - elapsed)
            
            if ((1.0/self.ctrl_freq) - elapsed) < 0:
                print("Control frequency is too high")

            start = time.time()

def main(max_quad = None):
    ports = io.get_available_ports()
    if not ports:
        raise IOError('No port available.')
    
    ctrl_freq = 100

    if max_quad is not None:
        ports = ports[:max_quad]

    MQ = MultiQuad(ports, ctrl_freq)

    MQ.neutral_controller()

    ctrl = [-0.6191339 , -0.00869758, 0.08034393, -0.34647357, -0.7816453 , 0.8126544 , -0.02539819, -0.03454808, 0.72835165, 0.2531592 , -0.10565615, 0.12811454, -0.5659985 , 0.00621947, -0.728982 , -0.3037064 ]

    MQ.run_new_sin_controller(ctrl, duration=4.0)
    MQ._exec_traj()
    MQ.shutdown()

if __name__ == "__main__":
    main()
