# SẢN PHẨM ĐỒ ÁN CUỐI KỲ MÔN NT230.O21.ANTT

## Code trong repo này sẽ huấn luyện mạng WGAN-GP và tạo ra các tên miền giả

Để huấn luyện mô hình, trước tiên cần trích xuất lấy tên miền của 1 tên miền đầy đủ. VD: google.com -> google
Sau đó lưu kết quả vào trong file benign.txt

### Trích xuất tên miền từ tên miền đầy đủ

```bash
python khaos/extract_sld.py BENIGN_FULL_DOMAIN_NAME OUTPUT_FILE
```

## #Huấn luyện mạng WGAN-GP với detector là LSTM-based model
```bash
python khaos/gan_language.py
```
Sau khi huấn luyện xong, Generator sẽ được lưu vào file khaos_lstm.trc

### Huấn luyện mạng WGAN-GP với detector là ResNet-based model
```bash
python khaos/khaos_original.py
```

Sau khi huấn luyện xong, Generator sẽ được lưu vào file khaos_resnet.trc

### Tạo ra các mẫu tên miền đầy đủ từ mô hình đã được huấn luyện và lưu lại
```bash
python khaos/gen_sample.py
```

Sau khi tạo xong, các tên miền sẽ được lưu trong file khaos_original_11000.txt

## Các nguồn tham khảo (bao gồm cả code lẫn tài liệu liên quan)

[1] X. Yun, J. Huang, Y. Wang, T. Zang, Y. Zhou, and Y. Zhang, “Khaos: An adversarial neural network dga with high anti-detection ability,” IEEE Trans. Inf. Forensics Secur., vol. 15, no. 1, pp. 2225–2240, 2020.

[2] https://github.com/caogang/wgan-gp/blob/master/README.md

[3] https://github.com/abcdefdf/PKDGA
