# Satu-Sama AI API Contract (Draft)

> **Frontend Developer Note**: 
> Base URL: `http://localhost:8000`
> 所有接口均在 swagger 上可见: `http://localhost:8000/docs`

## 1. Compliance (合规检测)

### 1.1 Text Check (文本检测)
**POST** `/api/v1/compliance/text-check`

用于检查商品标题、描述是否含有违禁词。

**Request Body**:
```json
{
  "text": "Best whitening cream ever, 100% cure guarantee!",
  "platform": "tiktok", // or "shopee", "jakim"
  "language": "en"
}
```

**Response**:
```json
{
  "score": 0.4, // 0-1, 1 is safe, 0 is risky
  "issues": [
    {
      "type": "prohibited_word",
      "word": "cure",
      "suggestion": "help improve",
      "source": "TikTok Shop Policy Section 3.2"
    }
  ]
}
```

### 1.2 Ingredient Check (成分检测 - 清真)
**POST** `/api/v1/compliance/ingredient-check`

**Request Body**:
```json
{
  "ingredients": ["Water", "Glycerin", "Carmine", "Alcohol"]
}
```

**Response**:
```json
{
  "halal_status": "non_halal", // safe, warning, non_halal
  "risky_ingredients": [
    {
      "name": "Carmine",
      "reason": "Insect-derived pigment, usually not Halal.",
      "reference": "JAKIM Fatwa 2021"
    }
  ]
}
```

## 2. Localization (本地化文案)

### 2.1 Generate Copy (生成文案)
**POST** `/api/v1/localization/generate`

**Request Body**:
```json
{
  "product_name": "Matte Lipstick",
  "features": ["Long lasting", "Waterproof"],
  "target_lang": "ms-MY", // Malay
  "tone": "energetic" // professional, casual, energetic
}
```

**Response**:
```json
{
  "generated_text": "Gincu Matte yang Tahan Lama! ... (Malay Content)",
  "cultural_notes": "Avoided using 'Pig' related metaphors."
}
```
