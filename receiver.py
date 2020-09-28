import requests
import sim
import time

class Receiver:
    def __init__(self):
        sim.simxFinish(-1)
        self.id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # Connect to CoppeliaSim

    def __exit__(self, *err):
        sim.simxFinish(-1)

    def verificaConexao(self):
        conectado = sim.simxGetConnectionId(self.id) != -1
        while not conectado:
            sim.simxFinish(-1)
            self.id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # Connect to CoppeliaSim
            conectado = sim.simxGetConnectionId(self.id) != -1

        return conectado

def main():
    print("Receiver inicializado")
    print("Para finalizar o programa pressione ctrl+q")
    receiver = Receiver()
    receiverConectado = receiver.verificaConexao()
    if receiverConectado:
        receiver.runInSynchronousMode = True
        sair = False
        print("Conectado com sucesso!")
        while receiverConectado and not sair:
            codigoRetorno, filePath = sim.simxGetAndClearStringSignal(receiver.id, 'sending-photo', sim.simx_opmode_streaming)
            # print(codigoRetorno, sim.simx_return_ok)
            if codigoRetorno == sim.simx_return_ok and filePath:
                with open(filePath.decode("utf-8"), 'rb') as f:
                    r = requests.post('http://localhost:8080/store_photo', files={'image': f})
                # receiver.enviarFoto(corElemento)

            time.sleep(0.05)
            
            receiverConectado = receiver.verificaConexao()

        if sair:
            print("Programa finalizado!")

if __name__ == "__main__":
    main()