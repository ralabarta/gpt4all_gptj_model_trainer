import os
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    TextDataset, DataCollatorForLanguageModeling,
    Trainer, TrainingArguments
)


# Crear el modelo y el tokenizador
model_name = "nomic-ai/gpt4all-j", revision="v1.3-groovy"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Preparar el conjunto de datos
dataset_file = "https://drive.google.com/file/d/1UWd_eVcETmjT9Tsb7QgNwyKFjJz6WAvQ/view?usp=share_link"
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=dataset_file,
    block_size=128
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Configurar los argumentos de entrenamiento
output_dir = "output"
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=0.5,
    per_device_train_batch_size=4,
    save_steps=2_000,
    save_total_limit=2,
)

# Entrenar el modelo
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

trainer.train()

# Guardar el modelo y el tokenizador
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
