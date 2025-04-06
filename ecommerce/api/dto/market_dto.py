from typing import Optional, Dict

class MarketDTO:
  def __init__(self, id: Optional[int] = None, name: Optional[str] = None):
    self.id = id
    self.name = name

  @classmethod
  def from_model(cls, market) -> 'MarketDTO':
    return cls(
      id=market.id,
      name=market.name
    )

  def to_dict(self) -> Dict[str, Optional[str]]:
    return {
      'id': self.id,
      'name': self.name
    }

  def __str__(self) -> str:
    return f"MarketDTO(id={self.id}, name={self.name})"

  # التحقق من حقل الاسم ليس فارغ
  def is_valid(self) -> bool:
    if not self.name:
        return False
    return True
