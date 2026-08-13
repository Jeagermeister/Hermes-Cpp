# fsops scoreboard - 20260813T000201Z

Machine **cachyos-x8664** · GPU **NVIDIA RTX 5080 Laptop 16GB** · num_ctx **65536** · repeats **3** · sampling **model default**

Cell = passed / valid runs. A run passes only if every assertion holds **and** no unauthorised file was touched.

| task | llama32-3b | qwen-4b | qwen-9b |
|---|---|---|---|
| 01_create_file | 3/3 | 3/3 | 3/3 |
| 02_make_dirs | 2/3 | 3/3 | 2/3 |
| 03_move_file | 0/3 | 2/2 | 2/3 |
| 04_rename | 0/3 | 2/3 | 2/3 |
| 05_copy | 1/3 | 3/3 | 3/3 |
| 06_selective_delete | 0/3 | 2/3 | 2/3 |
| 07_run_script | 1/3 | 3/3 | 2/3 |
| 08_write_and_run_script | 0/3 | 2/2 | 2/3 |
| 09_list_report | 2/3 | 3/3 | 1/3 |
| 10_bulk_move | 0/3 | 2/2 | 3/3 |
| 11_append_preserve | 0/3 | 0/1 | 2/2 |
| 12_multi_step | 0/3 | 1/3 | 3/3 |
| **total** | **9/36** | **26/31** | **27/35** |

No collateral damage recorded in this run.
