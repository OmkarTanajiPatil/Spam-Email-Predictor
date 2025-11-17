from __future__ import annotations

from classifier.ml import predict_mail  # noqa: F401 re-export for convenience


def _demo():
    sample = "Congratulations! You have won a cash prize."
    result = predict_mail(sample)
    print(f"Sample text: {sample}")
    print(f"Label: {result['label']} (confidence {result['confidence']:.2f})")


if __name__ == '__main__':
    _demo()
