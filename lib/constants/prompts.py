# prompts.py

# General Tone
ARABIC_BLOOD_TEST_GENERAL_PROMPT = """
حلل نتائج اختبار الدم التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبار الدم.
- "lifestyle_changes": قائمة بالتغييرات المقترحة في نمط الحياة لتحسين النتائج.
- "diet_routine": قائمة بالتوصيات الغذائية بناءً على النتائج.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""
ENGLISH_BLOOD_TEST_GENERAL_PROMPT = """
Analyze the following blood test results and provide a response in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the blood test results.
- "lifestyle_changes": A list of suggested lifestyle changes to improve the results.
- "diet_routine": A list of dietary recommendations based on the results.

Blood test results:
{blood_test_text}

JSON:
"""

# General Doctor
ARABIC_BLOOD_TEST_DOCTOR_PROMPT = """
حلل نتائج اختبار الدم التالية بدقة واهتمام، وقدم استجابة مفصلة باللغة العربية بتنسيق JSON، كما لو كنت طبيبًا عامًا محترفًا.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص تفصيلي لنتائج اختبار الدم، مع شرح واضح لأي قيم غير طبيعية وتأثيراتها المحتملة على الصحة.
- "detailed_analysis": تحليل مفصل لكل مكون من مكونات اختبار الدم، مع مقارنة بالقيم المرجعية وشرح لأي انحرافات.
- "potential_causes": قائمة بالأسباب المحتملة لأي نتائج غير طبيعية، مع الأخذ في الاعتبار الأعراض المحتملة.
- "lifestyle_changes": توصيات محددة لتغييرات نمط الحياة لتحسين النتائج، مع شرح لأهمية كل تغيير.
- "diet_routine": توصيات غذائية مفصلة بناءً على النتائج، مع أمثلة على الأطعمة الموصى بها وتلك التي يجب تجنبها.
- "next_steps": توصيات للخطوات التالية، مثل استشارة أخصائي أو إجراء اختبارات إضافية.
- "disclaimer": تنويه بأن هذا التحليل هو لأغراض المعلومات فقط ولا يغني عن استشارة الطبيب.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""
ENGLISH_BLOOD_TEST_DOCTOR_PROMPT = """
Analyze the following blood test results with precision and care, and provide a detailed response in JSON format, as if you were a professional general doctor.
The JSON should contain the following keys:
- "summary": A detailed summary of the blood test results, with clear explanations of any abnormal values and their potential health implications.
- "detailed_analysis": A detailed analysis of each component of the blood test, with comparisons to reference ranges and explanations of any deviations.
- "potential_causes": A list of potential causes for any abnormal results, considering potential symptoms.
- "lifestyle_changes": Specific recommendations for lifestyle changes to improve the results, with explanations of the importance of each change.
- "diet_routine": Detailed dietary recommendations based on the results, with examples of recommended and avoided foods.
- "next_steps": Recommendations for next steps, such as specialist consultation or additional testing.
- "disclaimer": A disclaimer stating that this analysis is for informational purposes only and does not replace medical advice.

Blood test results:
{blood_test_text}

JSON:
"""

# Excuative summary
ENGLISH_BLOOD_TEST_EXECUTIVE_PROMPT = """
Provide an executive summary of the following blood test results in JSON format.
The JSON should contain the following keys:
- "key_findings": A list of the most significant findings from the blood test.
- "potential_impact": A brief description of the potential impact of these findings on the user's health.
- "recommendations": A list of actionable recommendations for the user.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_EXECUTIVE_PROMPT = """
قدم ملخصًا تنفيذيًا لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "key_findings": قائمة بأهم النتائج من اختبار الدم.
- "potential_impact": وصف موجز للتأثير المحتمل لهذه النتائج على صحة المستخدم.
- "recommendations": قائمة بالتوصيات القابلة للتنفيذ للمستخدم.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Educational/Informative
ENGLISH_BLOOD_TEST_EDUCATIONAL_PROMPT = """
Provide an educational analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "result_explanations": Detailed explanations of each blood test component and its significance.
- "reference_ranges": A comparison of the user's results to normal reference ranges.
- "potential_implications": An explanation of the potential health implications of any abnormal results.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_EDUCATIONAL_PROMPT = """
قدم تحليلاً تعليميًا لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "result_explanations": شروحات مفصلة لكل مكون من مكونات اختبار الدم وأهميته.
- "reference_ranges": مقارنة لنتائج المستخدم بالنطاقات المرجعية الطبيعية.
- "potential_implications": شرح للتأثيرات الصحية المحتملة لأي نتائج غير طبيعية.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Preventative/Wellness
ENGLISH_BLOOD_TEST_PREVENTATIVE_PROMPT = """
Provide a preventative/wellness-focused analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "wellness_assessment": An assessment of the user's overall wellness based on the results.
- "preventative_recommendations": Recommendations for lifestyle and dietary changes to maintain or improve health.
- "long_term_outlook": A discussion of the long-term health implications of the results.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_PREVENTATIVE_PROMPT = """
قدم تحليلاً يركز على الوقاية والعافية لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "wellness_assessment": تقييم لعافية المستخدم العامة بناءً على النتائج.
- "preventative_recommendations": توصيات لتغييرات نمط الحياة والنظام الغذائي للحفاظ على الصحة أو تحسينها.
- "long_term_outlook": مناقشة للتأثيرات الصحية طويلة المدى للنتائج.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Technical/Scientific
ENGLISH_BLOOD_TEST_TECHNICAL_PROMPT = """
Provide a technical/scientific analysis of the following blood test results in JSON format.
Synthesize the information from general medical knowledge and avoid directly quoting copyrighted material.
Explain the results using your own words.
The JSON should contain the following keys:
- "detailed_lab_values": Detailed analysis of each lab value and its clinical significance, explained in your own words.
- "scientific_references": General areas of medical research or guidelines that are relevant, but do not directly quote.
- "pathophysiological_explanations": Explanations of the underlying pathophysiological mechanisms, explained in your own words.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_TECHNICAL_PROMPT = """
قدم تحليلاً تقنياً/علمياً لنتائج اختبار الدم التالية بتنسيق JSON.
قم بتجميع المعلومات من المعرفة الطبية العامة وتجنب الاقتباس المباشر من المواد المحمية بحقوق الطبع والنشر.
اشرح النتائج بكلماتك الخاصة.
يجب أن يحتوي JSON على المفاتيح التالية:
- "detailed_lab_values": تحليل مفصل لكل قيمة معملية وأهميتها السريرية، مشروحة بكلماتك الخاصة.
- "scientific_references": مجالات عامة للبحث الطبي أو الإرشادات ذات الصلة، ولكن لا تقتبس مباشرة.
- "pathophysiological_explanations": شروحات للآليات الفيزيولوجية المرضية الأساسية، مشروحة بكلماتك الخاصة.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Personalized/Empathetic
ENGLISH_BLOOD_TEST_EMPATHETIC_PROMPT = """
Provide a personalized and empathetic analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "personal_summary": A summary of the results tailored to the user's specific concerns.
- "emotional_support": Empathetic and supportive language acknowledging the user's feelings.
- "individualized_recommendations": Recommendations tailored to the user's individual needs and circumstances.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_EMPATHETIC_PROMPT = """
قدم تحليلاً شخصيًا ومتعاطفًا لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "personal_summary": ملخص للنتائج مصمم خصيصًا لمخاوف المستخدم المحددة.
- "emotional_support": لغة متعاطفة وداعمة تعترف بمشاعر المستخدم.
- "individualized_recommendations": توصيات مصممة خصيصًا لتلبية احتياجات المستخدم الفردية وظروفه.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""