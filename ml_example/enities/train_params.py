from dataclasses import dataclass, field


@dataclass()
class TrainingParams:
    model_type: str = field(default="CatBoost")
    random_state: int = field(default=255)
    iterations: int = field(default=400)
    random_seed: int = field(default=42)
    learning_rate: int= field(default=0.005)
    custom_loss: list[str] = field(default_factory=['AUC', 'Accuracy','Recall'])
    use_best_model: bool = field(default=True)
    cat_features: list[int] = field(default_factory="[1,2,5,6,8,10,12]")#sex cp fbs restecg exang slope thal
