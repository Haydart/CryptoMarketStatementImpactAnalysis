from experiments.experiment_def import run_expreminent

run_expreminent(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2)
run_expreminent(look_back=2, hidden_size=4, batch_size=50, epochs=100, dropout=0.2)
run_expreminent(look_back=3, hidden_size=4, batch_size=50, epochs=100, dropout=0.2)