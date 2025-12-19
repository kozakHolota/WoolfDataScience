import os
import time
from tempfile import TemporaryDirectory

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

import torchvision
from torchvision import datasets, models, transforms

import matplotlib.pyplot as plt


# -------------------------
# 1) БАЗОВІ НАЛАШТУВАННЯ
# -------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# TODO: змініть на свій шлях
data_dir = "/path/to/data"  # <- наприклад: "./hymenoptera_data"

# Типові трансформації для ResNet (як у більшості туторіалів)
data_transforms = {
    "train": transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ]),
    "val": transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ]),
}

# Datasets + Dataloaders
image_datasets = {
    x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
    for x in ["train", "val"]
}

dataloaders = {
    x: torch.utils.data.DataLoader(
        image_datasets[x],
        batch_size=32,
        shuffle=True if x == "train" else False,
        num_workers=2,
        pin_memory=torch.cuda.is_available(),
    )
    for x in ["train", "val"]
}

dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "val"]}
class_names = image_datasets["train"].classes
num_classes = len(class_names)

print("Classes:", class_names)
print("Dataset sizes:", dataset_sizes)


# -------------------------
# 2) ДОПОМІЖНЕ: IMshow
# -------------------------
def imshow(inp, title=None):
    """
    inp: torch.Tensor CxHxW (нормалізований)
    """
    inp = inp.numpy().transpose((1, 2, 0))

    mean = np.array([0.485, 0.456, 0.406])
    std  = np.array([0.229, 0.224, 0.225])

    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)

    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)


# -------------------------
# 3) TRAIN + VAL (як у розділі)
# -------------------------
def train_model(model, criterion, optimizer, scheduler=None, num_epochs=25):
    since = time.time()

    with TemporaryDirectory() as tempdir:
        best_model_params_path = os.path.join(tempdir, "best_model_params.pt")
        torch.save(model.state_dict(), best_model_params_path)
        best_acc = 0.0

        for epoch in range(num_epochs):
            print(f"Epoch {epoch+1}/{num_epochs}")
            print("-" * 10)

            for phase in ["train", "val"]:
                if phase == "train":
                    model.train()
                else:
                    model.eval()

                running_loss = 0.0
                running_corrects = 0

                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        if phase == "train":
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

                # у розділі best зберігається за val accuracy
                if phase == "val" and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    torch.save(model.state_dict(), best_model_params_path)

            # типово scheduler крокають раз на епоху (часто після train)
            if scheduler is not None:
                scheduler.step()

            print()

        time_elapsed = time.time() - since
        print(f"Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
        print(f"Best val Acc: {best_acc:.6f}")

        model.load_state_dict(torch.load(best_model_params_path, map_location=device))

    return model


def visualize_model(model, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0

    plt.figure(figsize=(8, 8))

    with torch.no_grad():
        for inputs, labels in dataloaders["val"]:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            for j in range(inputs.size(0)):
                images_so_far += 1
                ax = plt.subplot(num_images // 2, 2, images_so_far)
                ax.axis("off")

                pred_name = class_names[preds[j].item()]
                true_name = class_names[labels[j].item()]
                ax.set_title(f"pred: {pred_name}\ntrue: {true_name}")

                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    plt.show()
                    return

    model.train(mode=was_training)
    plt.show()


# -------------------------
# 4) ПІДХІД 1 — ТРЕНУЄМО ВСІ ВАГИ
# -------------------------
model_ft = models.resnet18(weights="IMAGENET1K_V1")
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, num_classes)
model_ft = model_ft.to(device)

criterion = nn.CrossEntropyLoss()

# Важливо: оптимізуємо ВСІ параметри
optimizer_ft = optim.Adam(model_ft.parameters(), lr=1e-5)

# Приклад exp_lr_scheduler (можна змінити під себе)
exp_lr_scheduler = optim.lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

model_ft = train_model(
    model_ft, criterion, optimizer_ft,
    scheduler=exp_lr_scheduler,
    num_epochs=5
)

visualize_model(model_ft, num_images=6)


# -------------------------
# 5) ПІДХІД 2 — ЗАМОРОЖУЄМО ВАГИ, ТРЕНУЄМО ЛИШЕ FC
# -------------------------
model_conv = torchvision.models.resnet18(weights="IMAGENET1K_V1")

for param in model_conv.parameters():
    param.requires_grad = False

num_ftrs = model_conv.fc.in_features
model_conv.fc = nn.Linear(num_ftrs, num_classes)  # цей шар має requires_grad=True за замовчуванням
model_conv = model_conv.to(device)

criterion = nn.CrossEntropyLoss()

# Важливо: оптимізуємо тільки fc
optimizer_conv = optim.Adam(model_conv.fc.parameters(), lr=1e-3)

# Scheduler опційно
exp_lr_scheduler2 = optim.lr_scheduler.StepLR(optimizer_conv, step_size=7, gamma=0.1)

model_conv = train_model(
    model_conv, criterion, optimizer_conv,
    scheduler=exp_lr_scheduler2,
    num_epochs=5
)

visualize_model(model_conv, num_images=6)
