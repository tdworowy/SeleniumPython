echo "export PYTHONPATH=" > ~/.bashrc
echo "export PYTHONPATH=${PYTHONPATH}:..\${PWD}" >> ~/.bashrc
cp get_songs_from_last_fm.py /home/tom/airflow/dags/