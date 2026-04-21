import torch

print(f"Pytorch Version: {torch.__version__}")

print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"torch version: {torch.version.cuda}") 
