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


# New Prompts
ARABIC_CBC_PROMPT = """
بصفتك {tone}، حلل نتائج فحص تعداد الدم الكامل (CBC) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحص تعداد الدم الكامل، مع الإشارة إلى أي قيم خارج النطاق الطبيعي.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل فقر الدم، الالتهابات، إلخ).
- "next_steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج فحص تعداد الدم الكامل:
{blood_test_text}

JSON:
"""
ENGLISH_CBC_PROMPT = """
As a {tone}, analyze the following Complete Blood Count (CBC) results and provide a response in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the CBC results, highlighting any values outside the normal range.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., anemia, infections, etc.).
- "next_steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Complete Blood Count results:
{blood_test_text}

JSON:
"""

ARABIC_COMPARE_PROMPT = """
بصفتك {tone}، قارن بين نتائج تقارير اختبارات الدم المتعددة التالية وقدم باللغة العربية ملخصًا للتقدم أو التغييرات الملحوظة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "comparison_summary": ملخص لأوجه التشابه والاختلاف والاتجاهات الرئيسية بين التقارير المقدمة.
- "parameter_changes": تفصيل للتغيرات الهامة في قيم المعلمات الرئيسية عبر التقارير (زيادة أو نقصان).
- "overall_progress": تقييم عام للتقدم أو التغييرات في صحة المريض بناءً على مقارنة التقارير.
- "recommendations": توصيات بناءً على مقارنة التقارير، مثل الاستمرار في الخطة الحالية أو إجراء تعديلات.

تقارير اختبارات الدم:
{blood_test_text}

JSON:
"""
ENGLISH_COMPARE_PROMPT = """
As a {tone}, compare the results of the following multiple blood test reports and provide a progress summary in English in JSON format.
The JSON should contain the following keys:
- "comparison_summary": A summary of the similarities, differences, and key trends across the provided reports.
- "parameter_changes": Details of significant changes in key parameter values across the reports (increases or decreases).
- "overall_progress": An overall assessment of the progress or changes in the patient's health based on the report comparison.
- "recommendations": Recommendations based on the comparison, such as continuing the current plan or making adjustments.

Blood test reports:
{blood_test_text}

JSON:
"""

ARABIC_GLUCOSE_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار مستوى السكر في الدم (صائم أو عشوائي) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "glucose_level": قيمة مستوى السكر في الدم.
- "interpretation": تفسير للنتيجة بناءً على ما إذا كان الاختبار صائمًا أم عشوائيًا، مع الإشارة إلى النطاقات الطبيعية وما إذا كانت النتيجة تشير إلى سكري أو مقدمات سكري أو طبيعية.
- "recommendations": توصيات بناءً على النتيجة، مثل مراقبة مستويات السكر، استشارة الطبيب، أو إجراء اختبارات إضافية (مثل HbA1c).

نتيجة اختبار مستوى السكر في الدم:
{blood_test_text}
نوع الاختبار: (صائم/عشوائي)

JSON:
"""
ENGLISH_GLUCOSE_PROMPT = """
As a {tone}, analyze the following blood glucose test result (fasting or random) and provide a response in English in JSON format.
The JSON should contain the following keys:
- "glucose_level": The blood glucose level value.
- "interpretation": An interpretation of the result based on whether it was a fasting or random test, referencing normal ranges and indicating if the result suggests diabetes, pre-diabetes, or is normal.
- "recommendations": Recommendations based on the result, such as monitoring glucose levels, consulting a doctor, or further testing (e.g., HbA1c).

Blood glucose test result:
{blood_test_text}
Test type: (Fasting/Random)

JSON:
"""

ARABIC_LIVER_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الكبد (LFTs) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الكبد، مع الإشارة إلى أي قيم خارج النطاق الطبيعي (ALT، AST، ALP، بيليروبين).
- "affected_markers": قائمة بالعلامات الحيوية الكبدية التي أظهرت قيمًا غير طبيعية.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل التهاب الكبد، تلف الكبد).
- "next_steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الكبد:
{blood_test_text}

JSON:
"""
ENGLISH_LIVER_PROMPT = """
As a {tone}, analyze the following Liver Function Tests (LFTs) results and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the LFTs results, highlighting any values outside the normal range (ALT, AST, ALP, Bilirubin).
- "affected_markers": A list of the liver function markers that showed abnormal values.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., hepatitis, liver damage).
- "next_steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Liver Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_KIDNEY_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الكلى التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الكلى، مع الإشارة إلى قيم الكرياتينين ونيتروجين اليوريا في الدم (BUN) وما إذا كانت ضمن النطاق الطبيعي.
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى وجود مشاكل في وظائف الكلى.
- "recommendations": توصيات بناءً على النتائج، مثل مراقبة وظائف الكلى، استشارة الطبيب، أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الكلى:
{blood_test_text}

JSON:
"""
ENGLISH_KIDNEY_PROMPT = """
As a {tone}, analyze the following Kidney Function Tests results and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the kidney function tests results, highlighting the Creatinine and Blood Urea Nitrogen (BUN) values and whether they are within the normal range.
- "interpretation": An interpretation of the results and whether they suggest any issues with kidney function.
- "recommendations": Recommendations based on the results, such as monitoring kidney function, consulting a doctor, or further testing.

Kidney Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_LIPID_PROMPT = """
بصفتك {tone}، حلل نتائج فحص الدهون (الكوليسترول) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحص الدهون، مع الإشارة إلى قيم الكوليسترول الكلي، والكوليسترول الضار (LDL)، والكوليسترول الجيد (HDL)، والدهون الثلاثية وما إذا كانت ضمن النطاقات الصحية.
- "risk_assessment": تقييم لمخاطر الإصابة بأمراض القلب والسكتة الدماغية بناءً على مستويات الدهون.
- "recommendations": توصيات بناءً على النتائج، مثل تغييرات في نمط الحياة، النظام الغذائي، أو استشارة الطبيب بشأن العلاج.

نتائج فحص الدهون:
{blood_test_text}

JSON:
"""
ENGLISH_LIPID_PROMPT = """
As a {tone}, analyze the following Lipid Profile (Cholesterol Test) results and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the lipid profile results, highlighting the values for Total Cholesterol, LDL (bad cholesterol), HDL (good cholesterol), and Triglycerides and whether they are within healthy ranges.
- "risk_assessment": An assessment of the risk for heart disease and stroke based on the lipid levels.
- "recommendations": Recommendations based on the results, such as lifestyle changes, dietary modifications, or consulting a doctor about treatment.

Lipid Profile results:
{blood_test_text}

JSON:
"""

ARABIC_HBA1C_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار الهيموجلوبين السكري (HbA1c) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "hba1c_level": قيمة مستوى الهيموجلوبين السكري.
- "average_glucose": تقدير لمستوى السكر في الدم المتوسط على مدى 2-3 أشهر الماضية بناءً على نتيجة HbA1c.
- "interpretation": تفسير للنتيجة وما إذا كانت تشير إلى تحكم جيد في السكر، أو مقدمات سكري، أو سكري.
- "recommendations": توصيات بناءً على النتيجة، خاصة لمرضى السكري بشأن إدارة مستويات السكر في الدم.

نتيجة اختبار الهيموجلوبين السكري (HbA1c):
{blood_test_text}

JSON:
"""
ENGLISH_HBA1C_PROMPT = """
As a {tone}, analyze the following Hemoglobin A1c (HbA1c) test result and provide a response in English in JSON format.
The JSON should contain the following keys:
- "hba1c_level": The Hemoglobin A1c level value.
- "average_glucose": An estimation of the average blood glucose level over the past 2-3 months based on the HbA1c result.
- "interpretation": An interpretation of the result and whether it indicates good blood sugar control, pre-diabetes, or diabetes.
- "recommendations": Recommendations based on the result, especially for diabetic patients regarding blood sugar management.

Hemoglobin A1c (HbA1c) result:
{blood_test_text}

JSON:
"""

ARABIC_VITAMIN_D_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار فيتامين د (25-هيدروكسي فيتامين د) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "vitamin_d_level": قيمة مستوى فيتامين د.
- "interpretation": تفسير للنتيجة وما إذا كانت تشير إلى نقص حاد، نقص، اكتفاء، أو مستويات عالية من فيتامين د.
- "potential_implications": شرح محتمل لتأثير مستويات فيتامين د على صحة العظام ووظيفة المناعة.
- "recommendations": توصيات بناءً على النتيجة، مثل تناول مكملات فيتامين د أو التعرض لأشعة الشمس.

نتيجة اختبار فيتامين د (25-هيدروكسي فيتامين د):
{blood_test_text}

JSON:
"""
ENGLISH_VITAMIN_D_PROMPT = """
As a {tone}, analyze the following Vitamin D Test (25-hydroxy Vitamin D) result and provide a response in English in JSON format.
The JSON should contain the following keys:
- "vitamin_d_level": The Vitamin D level value.
- "interpretation": An interpretation of the result and whether it indicates severe deficiency, deficiency, sufficiency, or high levels of Vitamin D.
- "potential_implications": Potential explanations for the impact of the Vitamin D level on bone health and immune function.
- "recommendations": Recommendations based on the result, such as taking Vitamin D supplements or sun exposure.

Vitamin D Test (25-hydroxy Vitamin D) result:
{blood_test_text}

JSON:
"""

ARABIC_THYROID_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الغدة الدرقية التالية (TSH، T3، T4) وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الغدة الدرقية، مع الإشارة إلى قيم TSH، T3، و T4 وما إذا كانت ضمن النطاقات الطبيعية.
- "affected_hormones": قائمة بالهرمونات الدرقية التي أظهرت قيمًا غير طبيعية.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل قصور الغدة الدرقية أو فرط نشاط الغدة الدرقية).
- "next_steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الغدة الدرقية:
{blood_test_text}

JSON:
"""
ENGLISH_THYROID_PROMPT = """
As a {tone}, analyze the following Thyroid Function Tests results (TSH, T3, and T4) and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the thyroid function tests results, highlighting the values for TSH, T3, and T4 and whether they are within normal ranges.
- "affected_hormones": A list of the thyroid hormones that showed abnormal values.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., hypothyroidism or hyperthyroidism).
- "next_steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Thyroid Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_IRON_PROMPT = """
بصفتك {tone}، حلل نتائج فحوصات الحديد (الحديد والفيريتين) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحوصات الحديد، مع الإشارة إلى قيم الحديد والفيريتين وما إذا كانت ضمن النطاقات الطبيعية.
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى نقص الحديد (فقر الدم الناجم عن نقص الحديد) أو زيادة الحديد.
- "recommendations": توصيات بناءً على النتائج، مثل تغييرات في النظام الغذائي أو تناول مكملات الحديد أو إجراء فحوصات إضافية.

نتائج فحوصات الحديد (الحديد والفيريتين):
{blood_test_text}

JSON:
"""
ENGLISH_IRON_PROMPT = """
As a {tone}, analyze the following Iron Studies (Iron & Ferritin) results and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the iron studies results, highlighting the Iron and Ferritin values and whether they are within normal ranges.
- "interpretation": An interpretation of the results and whether they suggest iron deficiency (iron deficiency anemia) or iron overload.
- "recommendations": Recommendations based on the results, such as dietary changes, iron supplementation, or further testing.

Iron Studies (Iron & Ferritin) results:
{blood_test_text}

JSON:
"""

ARABIC_INFLAMMATION_PROMPT = """
بصفتك {tone}، حلل نتائج علامات الالتهاب (CRP و ESR) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج علامات الالتهاب، مع الإشارة إلى قيم CRP و ESR وما إذا كانت مرتفعة.
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى وجود التهاب في الجسم.
- "potential_causes": ذكر بعض الأسباب المحتملة لارتفاع علامات الالتهاب (مثل العدوى، أمراض المناعة الذاتية).
- "next_steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب لتحديد سبب الالتهاب.

نتائج علامات الالتهاب (CRP و ESR):
{blood_test_text}

JSON:
"""
ENGLISH_INFLAMMATION_PROMPT = """
As a {tone}, analyze the following Inflammation Markers (CRP and ESR) results and provide a response in English in JSON format.
The JSON should contain the following keys:
- "summary": A concise summary of the inflammation markers results, highlighting the CRP and ESR values and whether they are elevated.
- "interpretation": An interpretation of the results and whether they suggest the presence of inflammation in the body.
- "potential_causes": Mention some potential underlying causes for elevated inflammation markers (e.g., infection, autoimmune conditions).
- "next_steps": Recommendations for the next steps based on the results, such as consulting a doctor to determine the cause of inflammation.

Inflammation Markers (CRP and ESR) results:
{blood_test_text}

JSON:
"""