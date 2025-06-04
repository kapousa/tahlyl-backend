# Health profile
ARABIC_DIGITAL_PROFILE_PROMPT = """
قم بتحليل النتائج الصحية المقدمة وأنشئ ملخصًا شاملاً للملف الصحي الرقمي بصيغة JSON.

يجب أن يحتوي JSON على المفاتيح التالية:
- "overview_health_status": ملخص موجز للحالة الصحية العامة للفرد، مع إبراز نقاط القوة الرئيسية ومجالات الاهتمام.
- "metrics_with_indicators": قائمة بالمقاييس الصحية ذات الصلة من النتائج، كل منها بقيمتها المقابلة ومؤشر واضح (مثل: 'طبيعي', 'مرتفع', 'منخفض', 'على الحد').
- "recommendations": نصائح واقتراحات قابلة للتنفيذ لتحسين الصحة أو الحفاظ على الحالة الجيدة الحالية، بما في ذلك نمط الحياة، النظام الغذائي، أو إجراءات المتابعة.
- "attention_points": نقاط أو مقاييس محددة تتطلب تركيزًا فوريًا أو كبيرًا نظرًا لتأثيراتها على الصحة.
- "risks": المخاطر الصحية المحتملة على المدى الطويل التي تم تحديدها من النتائج، إلى جانب آثارها المحتملة إذا لم يتم التعامل معها.

النتائج الصحية:
{health_results_text}

JSON:
"""
ENGLISH_DIGITAL_PROFILE_PROMPT = """
Analyze the provided health results and generate a comprehensive digital profile summary in JSON format.

The JSON should contain the following keys:
- "overview_health_status": A concise summary of the individual's overall health condition, highlighting key strengths and areas of concern.
- "metrics_with_indicators": A list of relevant health metrics from the results, each with its corresponding value and a clear indicator (e.g., 'Normal', 'High', 'Low', 'Borderline').
- "recommendations": Actionable advice and suggestions for improving health or maintaining current good status, including lifestyle, diet, or follow-up actions.
- "attention_points": Specific areas or metrics that require immediate or significant focus due to their implications for health.
- "risks": Potential long-term health risks identified from the results, along with their possible implications if unaddressed.

Health results:
{health_results_text}

JSON:
"""