## Benchmarking FastAPI endpoints

FastAPI offers async/sync functionality. This can be achieved by defining endpoints as `def` or `async def` depending on the type of workload. 
In real scenarios the type of workload is mixed i.e. both CPU bound and IO bound workload, in such cases it might be useful to offload CPU bound tasks to another thread/process. 

We also know that Python is notoriously famous for its inability to exploit multithreading however at the same time being a master of asynchronous control. Due to all these reasons I decided to benchmark various ways of writing endpoints which process both CPU-bound & IO bound workloads. 

The benchmarking is done using **apache benchmark** which can be easily installed on linux platforms. 

### Set up project requirements
```bash
pip install pip-tools && make requirements
```

### Start local server
```bash
make local-server
```

### Benchmark a specific endpoint 
```bash
make benchmark-endpoint url=http://localhost:8000/test file=test
```
The above command saves the benchmark results under the folder `benchmark/test.txt`

### Benchmark all endpoints 
```bash
make benchmark
```
The above command writes the results under the folder `benchmark/`
