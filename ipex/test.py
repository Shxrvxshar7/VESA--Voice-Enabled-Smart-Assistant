import torch
import intel_extension_for_pytorch as ipex

x = torch.randn(3, 3)
x = x.to(ipex.DEVICE)
print(x)
