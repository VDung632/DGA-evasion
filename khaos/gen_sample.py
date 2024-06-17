# from khaos.gan_language import Generator
import sys
sys.path.insert(0, "../")

import re
import torch
import numpy as np
import torch.autograd as autograd
import khaos.N_gram as N_gram
from memory_profiler import profile
import torch.nn as nn
from fqdn import FQDN
import tldextract
import random

# Trong script này mặc định tập tên miền lành tính được đưa vào
# chỉ có domain name hoặc đã được tách TLD ra, VD: google, youtube, github, v.v.
# Ví dụ các tên miền không hợp lệ: google.com, youtube.com, v.v.
# Các tên miền không nên chứa sublevel domain do tính năng này chưa được kiểm thử.

# Trước khi chạy file, đưa tất cả các tên miền lành tính vào file benign.txt


use_cuda = False
if use_cuda:
    gpu = 0
Sample_num = 11000 # Số lượng tên miền tạo ra
SEQ_LEN = 10
BATCH_SIZE = 64  # Batch size
ITERS = 55  # How many iterations to train for
# SEQ_LEN = 10  # Sequence length in characters
DIM = 64  # Model dimensionality. This is fairly slow and overfits, even on
          # Billion Word. Consider decreasing for smaller datasets.
CRITIC_ITERS = 156 # How many critic iterations per generator iteration. We
                  # use 10 for the results in the paper, but 5 should work fine
                  # as well.
LAMBDA = 10  # Gradient penalty lambda hyperparameter.
MAX_N_EXAMPLES = 10000  # 10000000 # Max number of data examples to load. If data loading
                          # is too slow or takes too much RAM, you can decrease
                          # this (at the expense of having less training data).
class ResBlock(nn.Module):

    def __init__(self):
        super(ResBlock, self).__init__()

        self.res_block = nn.Sequential(
            nn.ReLU(True),
            nn.Conv1d(DIM, DIM, 3, padding=1),  # nn.Linear(DIM, DIM),
            nn.ReLU(True),
            nn.Conv1d(DIM, DIM, 3, padding=1),  # nn.Linear(DIM, DIM),
        )

    def forward(self, input):
        output = self.res_block(input)
        return input + (0.3*output)


class Generator(nn.Module):

    def __init__(self):
        super(Generator, self).__init__()

        self.fc1 = nn.Linear(5000, DIM*SEQ_LEN)

        self.block = nn.Sequential(
            ResBlock(),
            ResBlock(),
            ResBlock(),
        )
        self.conv1 = nn.Conv1d(DIM, 5000, 1)
        self.softmax = nn.Softmax()

    def forward(self, noise):
        output = self.fc1(noise)
        output = output.view(-1, DIM, SEQ_LEN)  # (BATCH_SIZE, DIM, SEQ_LEN)
        output = self.block(output)
        output = self.conv1(output)
        output = output.transpose(1, 2)
        shape = output.size()
        output = output.contiguous()
        output = output.view(BATCH_SIZE*SEQ_LEN, -1)
        output = self.softmax(output)
        return output.view(shape)  # (BATCH_SIZE, SEQ_LEN, len(charmap))

# Lọc theo độ dài
def valid_length(domain):
    return len(domain) >= 3

def valid_fqdn(domain):
    if is_full_domain(domain):
        return FQDN(domain).is_valid
    return True

def is_valid_domain(domain):
    domain_regex = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
    
    return domain_regex.match(domain)

def is_full_domain(domain):
    extracted = tldextract.extract(domain)
    return bool(extracted.domain) and bool(extracted.suffix)

def remove_duplicates(input_list):
    return np.unique(input_list).tolist()

def Domain_filter(domains):
    valid_domains = []
    for domain in domains:
        if valid_length(domain) and valid_fqdn(domain):
            valid_domains.append(domain)

    unique_valid_domains = remove_duplicates(valid_domains)

    return unique_valid_domains

def gen():
    netG = Generator()
    netG.load_state_dict(torch.load('./khaos_resnet.trc'))
    noise = torch.randn(Sample_num, 5000)
    # noise = noise.cuda(gpu)
    with torch.no_grad():
        noisev = autograd.Variable(noise, volatile=True)  # totally freeze netG
    print(noisev)
    samples = netG(noisev)
    samples = samples.view(-1, SEQ_LEN, 5000)
    samples = samples.cpu().data.numpy()
    
    #for sample in samples[:500]:
    #    print(len(sample))

    samples = np.argmax(samples, axis=2)
    new_str = N_gram.int_to_char(samples, False)

    return new_str

@profile
def write_to_file():
    gen_domains = gen()

    # danh sách các top level domain
    tlds = ['.com', '.org', '.net', '.edu', '.gov', '.int', '.info', '.biz']

    # Tạo seed để chọn ngẫu nhiên tên miền
    random.seed(123)

    filtered_domains = Domain_filter(gen_domains)
    while (True):
        filtered_domains = Domain_filter(filtered_domains)
        if len(filtered_domains) >= Sample_num:
            with open('./khaos_original_11000.txt', 'w') as f:
                for i in filtered_domains[:Sample_num]:
                    tld = random.choice(tlds)
                    domain = f"{i}{tld}"
                    f.write(domain + '\n')
            break
        else:
            filtered_domains += gen()
        
# Kết quả sẽ được lữu vào file khaos_original_11000.txt
write_to_file()