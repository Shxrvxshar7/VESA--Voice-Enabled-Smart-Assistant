from multiprocessing import Manager

manager = Manager()
shared_dict = manager.dict()

# Initialize shared state
shared_dict.update({
    'logs': [],
    'status': 'inactive',
    'last_transcription': '',
    'history': []
})