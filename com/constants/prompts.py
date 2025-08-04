# # prompts.py
#
# # General Tone (No specific status/range instructions added here as these are very general)
# ARABIC_BLOOD_TEST_GENERAL_PROMPT = """
# حلل نتائج اختبار الدم التالية وقدم باللغة العربية استجابة بتنسيق JSON.
# يجب أن يحتوي JSON على المفاتيح التالية:
# - "summary": ملخص موجز لنتائج اختبار الدم.
# - "lifestyle_changes": قائمة بالتغييرات المقترحة في نمط الحياة لتحسين النتائج.
# - "diet_routine": قائمة بالتوصيات الغذائية بناءً على النتائج.
# - **"doctor_questions": قائمة بالأسئلة التي يمكن طرحها على الطبيب بناءً على تحليل التقرير.**
#
# نتائج اختبار الدم:
# {blood_test_text}
#
# JSON:
# """
# ENGLISH_BLOOD_TEST_GENERAL_PROMPT = """
# Analyze the following blood test results and provide a response in JSON format.
# The JSON should contain the following keys:
# - "summary": A concise summary of the blood test results.
# - "lifestyle_changes": A list of suggested lifestyle changes to improve the results.
# - "diet_routine": A list of dietary recommendations based on the results.
# - **"doctor_questions": A list of questions to ask the doctor based on the report analysis.**
#
# Blood test results:
# {blood_test_text}
#
# JSON:
# """

# prompts.py

# General Tone (No specific status/range instructions added here as these are very general)
ARABIC_BLOOD_TEST_GENERAL_PROMPT = """
حلل نتائج اختبار الدم التالية وقدم باللغة العربية استجابة بتنسيق JSON.
يجب أن يحتوي JSON على كل المفاتيح الممكنة من المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبار الدم.
- "lifestyle_changes": قائمة بالتغييرات المقترحة في نمط الحياة لتحسين النتائج.
- "diet_routine": قائمة بالتوصيات الغذائية بناءً على النتائج.
- "key_findings": النتائج الرئيسية التي تم استخلاصها من التقرير.
- "potential_impact": التأثيرات المحتملة للنتائج على الصحة العامة.
- "recommendations": توصيات عامة إضافية.
- "detailed_analysis": تحليل مفصل لكل نتيجة اختبار.
- "potential_causes": الأسباب المحتملة وراء أي نتائج غير طبيعية.
- "next_steps": الخطوات التالية المقترحة بناءً على التحليل.
- "disclaimer": إخلاء مسؤولية يوضح أن التحليل ليس بديلاً عن الاستشارة الطبية المتخصصة.
- "result_explanations": شروحات مبسطة لمعنى كل نتيجة.
- "reference_ranges": النطاقات المرجعية الطبيعية لكل اختبار.
- "potential_implications": الآثار المحتملة على المدى القصير والطويل.
- "wellness_assessment": تقييم عام للحالة الصحية بناءً على النتائج.
- "preventative_recommendations": توصيات وقائية للحفاظ على الصحة.
- "long_term_outlook": نظرة مستقبلية طويلة المدى بناءً على النتائج.
- "detailed_lab_values": القيم المخبرية التفصيلية.
- "scientific_references": مراجع علمية تدعم التحليل (إن وجدت).
- "pathophysiological_explanations": تفسيرات فسيولوجية مرضية للنتائج.
- "personal_summary": ملخص شخصي موجه للمستخدم.
- "emotional_support": نصائح أو دعم عاطفي متعلق بالنتائج.
- "individualized_recommendations": توصيات فردية بناءً على ملف تعريف المستخدم.
- "date": تاريخ التحليل.
- "detailed_results": نتائج مفصلة لكل عنصر تم تحليله.
- "doctor_questions": قائمة بالأسئلة التي يمكن طرحها على الطبيب بناءً على تحليل التقرير.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""
ENGLISH_BLOOD_TEST_GENERAL_PROMPT = """
Analyze the following blood test results and provide a response in JSON format.
The JSON should contain all possible from the following keys:
- "summary": A concise summary of the blood test results.
- "lifestyle_changes": A list of suggested lifestyle changes to improve the results.
- "diet_routine": A list of dietary recommendations based on the results.
- "key_findings": Key findings extracted from the report.
- "potential_impact": Potential impacts of the results on overall health.
- "recommendations": Additional general recommendations.
- "detailed_analysis": A detailed analysis of each test result.
- "potential_causes": Potential causes behind any abnormal results.
- "next_steps": Suggested next steps based on the analysis.
- "disclaimer": A disclaimer stating that the analysis is not a substitute for professional medical advice.
- "result_explanations": Simplified explanations of what each result means.
- "reference_ranges": Normal reference ranges for each test.
- "potential_implications": Potential short-term and long-term implications.
- "wellness_assessment": A general wellness assessment based on the results.
- "preventative_recommendations": Preventative recommendations to maintain health.
- "long_term_outlook": A long-term outlook based on the results.
- "detailed_lab_values": Detailed laboratory values.
- "scientific_references": Scientific references supporting the analysis (if applicable).
- "pathophysiological_explanations": Pathophysiological explanations for the results.
- "personal_summary": A personalized summary tailored for the user.
- "emotional_support": Advice or emotional support related to the results.
- "individualized_recommendations": Individualized recommendations based on the user's profile.
- "date": Date of the analysis.
- "detailed_results": Detailed results for each analyzed item.
- "doctor_questions": A list of questions to ask the doctor based on the report analysis.

Blood test results:
{blood_test_text}

JSON:
"""

# General Doctor (No specific status/range instructions added here as these are very detailed)
# 'doctor_questions' removed as AI acts as the doctor here
ARABIC_BLOOD_TEST_DOCTOR_PROMPT = """
حلل نتائج اختبار الدم التالية بدقة واهتمام، وقدم استجابة مفصلة باللغة العربية بتنسيق JSON، كما لو كنت طبيبًا عامًا محترفًا.
يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص تفصيلي لنتائج اختبار الدم، مع شرح واضح لأي قيم غير طبيعية وتأثيراتها المحتملة على الصحة.
- "detailed_analysis": تحليل مفصل لكل مكون من مكونات اختبار الدم، مع مقارنة بالقيم المرجعية وشرح لأي انحرافات.
- "potential causes": قائمة بالأسباب المحتملة لأي نتائج غير طبيعية، مع الأخذ في الاعتبار الأعراض المحتملة.
- "lifestyle_changes": توصيات محددة لتغييرات نمط الحياة لتحسين النتائج، مع شرح لأهمية كل تغيير.
- "diet_routine": توصيات غذائية مفصلة بناءً على النتائج، مع أمثلة على الأطعمة الموصى بها وتلك التي يجب تجنبها.
- "next steps": توصيات للخطوات التالية، مثل استشارة أخصائي أو إجراء اختبارات إضافية.
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
- "next steps": Recommendations for next steps, such as specialist consultation or additional testing.
- "disclaimer": A disclaimer stating that this analysis is for informational purposes only and does not replace medical advice.

Blood test results:
{blood_test_text}

JSON:
"""

# Excuative summary (No specific status/range instructions added here as it's a brief summary)
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

# Educational/Informative (Focus on explaining ranges, so status is less critical here)
ARABIC_BLOOD_TEST_EDUCATIONAL_PROMPT = """
قدم تحليلاً تعليميًا لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "result_explanations": شروحات مفصلة لكل مكون من مكونات اختبار الدم وأهميته، بما في ذلك النطاقات الطبيعية النموذجية.
- "reference_ranges": مقارنة لنتائج المستخدم بالنطاقات المرجعية الطبيعية، مع ذكر هذه النطاقات صراحة.
- "potential_implications": شرح للتأثيرات الصحية المحتملة لأي نتائج غير طبيعية، مع الإشارة إلى كيفية انحرافها عن النطاقات الطبيعية.
- **"doctor_questions": قائمة بالأسئلة التي يمكن طرحها على الطبيب بناءً على تحليل التقرير.**

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""
ENGLISH_BLOOD_TEST_EDUCATIONAL_PROMPT = """
Provide an educational analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "result_explanations": Detailed explanations of each blood test component and its significance, including typical normal ranges.
- "reference_ranges": A comparison of the user's results to normal reference ranges, explicitly stating these ranges.
- "potential_implications": An explanation of the potential health implications of any abnormal results, referencing how they deviate from the normal ranges.
- **"doctor_questions": A list of questions to ask the doctor based on the report analysis.**

Blood test results:
{blood_test_text}

JSON:
"""

# Preventative/Wellness (Focus on overall assessment and recommendations)
ENGLISH_BLOOD_TEST_PREVENTATIVE_PROMPT = """
Provide a preventative/wellness-focused analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "wellness_assessment": An assessment of the user's overall wellness based on the results, noting any values outside typical healthy ranges.
- "preventative_recommendations": Recommendations for lifestyle and dietary changes to maintain or improve health, potentially referencing target ranges.
- "long_term_outlook": A discussion of the long-term health implications of the results, considering optimal ranges for wellness.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_PREVENTATIVE_PROMPT = """
قدم تحليلاً يركز على الوقاية والعافية لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "wellness_assessment": تقييم لعافية المستخدم العامة بناءً على النتائج، مع الإشارة إلى أي قيم خارج النطاقات الصحية النموذجية.
- "preventative_recommendations": توصيات لتغييرات نمط الحياة والنظام الغذائي للحفاظ على الصحة أو تحسينها، مع الإشارة المحتملة إلى النطاقات المستهدفة للعافية.
- "long_term_outlook": مناقشة للتأثيرات الصحية طويلة المدى للنتائج، مع الأخذ في الاعتبار النطاقات المثلى للعافية.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Technical/Scientific (Focus on detailed lab values and scientific context)
ENGLISH_BLOOD_TEST_TECHNICAL_PROMPT = """
Provide a technical/scientific analysis of the following blood test results in JSON format.
Synthesize the information from general medical knowledge and avoid directly quoting copyrighted material.
Explain the results using your own words, referencing typical normal ranges where relevant.
The JSON should contain the following keys:
- "detailed_lab_values": Detailed analysis of each lab value and its clinical significance, explained in your own words, including typical reference intervals.
- "scientific_references": General areas of medical research or guidelines that are relevant, but do not directly quote.
- "pathophysiological_explanations": Explanations of the underlying pathophysiological mechanisms, explained in your own words, potentially linking abnormal values to physiological processes.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_TECHNICAL_PROMPT = """
قدم تحليلاً تقنياً/علمياً لنتائج اختبار الدم التالية بتنسيق JSON.
قم بتجميع المعلومات من المعرفة الطبية العامة وتجنب الاقتباس المباشر من المواد المحمية بحقوق الطبع والنشر.
اشرح النتائج بكلماتك الخاصة، مع الإشارة إلى الفترات المرجعية الطبيعية النموذجية عند الاقتضاء.
يجب أن يحتوي JSON على المفاتيح التالية:
- "detailed_lab_values": تحليل مفصل لكل قيمة معملية وأهميتها السريرية، مشروحة بكلماتك الخاصة، بما في ذلك الفترات المرجعية النموذجية.
- "scientific_references": مجالات عامة للبحث الطبي أو الإرشادات ذات الصلة، ولكن لا تقتبس مباشرة.
- "pathophysiological_explanations": شروحات للآليات الفيزيولوجية المرضية الأساسية، مشروحة بكلماتك الخاصة، مع ربط القيم غير الطبيعية بالعمليات الفسيولوجية المحتملة.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""

# Personalized/Empathetic (Focus on individual concerns and support)
ENGLISH_BLOOD_TEST_EMPATHETIC_PROMPT = """
Provide a personalized and empathetic analysis of the following blood test results in JSON format.
The JSON should contain the following keys:
- "personal_summary": A summary of the results tailored to the user's specific concerns, acknowledging any values outside typical healthy ranges.
- "emotional_support": Empathetic and supportive language acknowledging the user's feelings about the results.
- "individualized_recommendations": Recommendations tailored to the user's individual needs and circumstances, potentially referencing target healthy ranges.

Blood test results:
{blood_test_text}

JSON:
"""
ARABIC_BLOOD_TEST_EMPATHETIC_PROMPT = """
قدم تحليلاً شخصيًا ومتعاطفًا لنتائج اختبار الدم التالية بتنسيق JSON.
يجب أن يحتوي JSON على المفاتيح التالية:
- "personal_summary": ملخص للنتائج مصمم خصيصًا لمخاوف المستخدم المحددة، مع الإشارة إلى أي قيم خارج النطاقات الصحية النموذجية.
- "emotional_support": لغة متعاطفة وداعمة تعترف بمشاعر المستخدم تجاه النتائج.
- "individualized_recommendations": توصيات مصممة خصيصًا لتلبية احتياجات المستخدم الفردية وظروفه، مع الإشارة المحتملة إلى النطاقات الصحية المستهدفة.

نتائج اختبار الدم:
{blood_test_text}

JSON:
"""


# New Prompts with status and ranges (COMPLETED SET)
ARABIC_CBC_PROMPT = """
بصفتك {tone}، حلل نتائج فحص تعداد الدم الكامل (CBC) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل معلمة من معلمات الدم، إذا كان هناك نطاق طبيعي متاح في نتيجة الاختبار أو من معرفتك الطبية، فيرجى تضمينه في JSON.
أيضًا، لكل قيمة رقمية، حدد ما إذا كانت "مرتفعة" أو "طبيعية" أو "منخفضة" بناءً على النطاق الطبيعي وقم بتضمين هذه "الحالة" في JSON لتلك المعلمة.

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحص تعداد الدم الكامل، مع الإشارة إلى أي قيم خارج النطاق الطبيعي وحالتها (مرتفعة أو منخفضة).
- "detailed_results": كائن تكون فيه كل مفتاح معلمة دم (مثل "خلايا الدم البيضاء" أو "خلايا الدم الحمراء") والقيمة هي كائن يحتوي على:
    - "value": القيمة المقاسة.
    - "unit": وحدة القياس (إذا تم توفيرها).
    - "normal_range": النطاق المرجعي الطبيعي (إذا تم توفيره أو معروف).
    - "status": "مرتفع", "طبيعي", أو "منخفض" بناءً على النطاق الطبيعي.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل فقر الدم إذا كانت خلايا الدم الحمراء منخفضة، والالتهابات إذا كانت خلايا الدم البيضاء مرتفعة، إلخ).
- "next steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج فحص تعداد الدم الكامل:
{blood_test_text}

JSON:
"""
ENGLISH_CBC_PROMPT = """
As a {tone}, analyze the following Complete Blood Count (CBC) results and provide a response in JSON format.
For each blood parameter, if a normal range is available in the test result or from your medical knowledge, please include it in the JSON.
Also, for each numerical value, determine if it is "high", "normal", or "low" based on the normal range and include this "status" in the JSON for that parameter.

The JSON should contain the following keys:
- "summary": A concise summary of the CBC results, highlighting any parameters that are outside the normal range and their status (high or low).
- "detailed_results": An object where each key is a blood parameter (e.g., "White Blood Cells", "Red Blood Cells") and the value is an object containing:
    - "value": The measured value.
    - "unit": The unit of measurement (if provided).
    - "normal_range": The normal reference range (if provided or known).
    - "status": "high", "normal", or "low" based on the normal range.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., anemia if red blood cells are low, infections if white blood cells are high, etc.).
- "next steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Complete Blood Count results:
{blood_test_text}

JSON:
"""

ARABIC_COMPARE_PROMPT = """
بصفتك {tone}، قارن بين نتائج تقارير اختبارات الدم المتعددة التالية وقدم باللغة العربية ملخصًا للتقدم أو التغييرات الملحوظة بتنسيق JSON.
لكل معلمة من معلمات الدم في كل تقرير، يجب أن يكون الذكاء الاصطناعي قد قام بتضمين النطاق الطبيعي والحالة ("مرتفع"، "طبيعي"، "منخفض") في استجابات JSON الأصلية.
عند المقارنة، سلط الضوء على ما إذا كانت المعلمة قد زادت أو نقصت بشكل ملحوظ أو ظلت مستقرة، وما إذا كانت حالتها قد تغيرت بين التقارير.

يجب أن يحتوي JSON على المفاتيح التالية:
- "comparison_summary": ملخص لأوجه التشابه والاختلاف والاتجاهات الرئيسية بين التقارير المقدمة.
- "report_comparisons": مصفوفة من الكائنات، حيث يقارن كل كائن نفس المعلمات عبر تقارير مختلفة. يمكن أن يحتوي كل كائن على مفاتيح مثل اسم المعلمة (مثل "الهيموجلوبين") ثم قيم تكون عبارة عن مصفوفات من الكائنات تحتوي على "value" و "unit" و "normal_range" و "status" من كل تقرير.
- "overall_progress": تقييم عام للتقدم أو التغييرات في صحة المريض بناءً على مقارنة التقارير.
- "recommendations": توصيات بناءً على مقارنة التقارير، مثل الاستمرار في الخطة الحالية أو إجراء تعديلات.

تقارير اختبارات الدم (بافتراض أن الاستجابات السابقة تضمنت نتائج مفصلة مع الحالة والنطاقات):
{blood_test_text}

JSON:
"""
ENGLISH_COMPARE_PROMPT = """
As a {tone}, compare the results of the following multiple blood test reports and provide a progress summary in English in JSON format.
For each blood parameter in each report, the AI should have included the normal range and status ("high", "normal", "low") in the original JSON responses.
When comparing, highlight if a parameter has significantly increased, decreased, or remained stable, and if its status has changed between the reports.

The JSON should contain the following keys:
- "comparison_summary": A summary of the key trends and changes across the provided reports.
- "report_comparisons": An array of objects, where each object compares the same parameters across different reports. Each object could have keys like the parameter name (e.g., "Hemoglobin") and then values that are arrays of objects containing "value", "unit", "normal_range", and "status" from each report.
- "overall_progress": An overall assessment of the progress or changes in the patient's health based on the report comparison.
- "recommendations": Recommendations based on the comparison, such as continuing the current plan or making adjustments.

Blood test reports (assuming previous responses included detailed results with status and ranges):
{blood_test_text}

JSON:
"""

ARABIC_GLUCOSE_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار مستوى السكر في الدم (صائم أو عشوائي) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
قم بتضمين النطاق الطبيعي لاختبار الجلوكوز الصائم أو العشوائي (حسب الاقتضاء) في JSON.
حدد "الحالة" ("مرتفع" أو "طبيعي" أو "منخفض") لمستوى الجلوكوز بناءً على هذه النطاقات.

يجب أن يحتوي JSON على المفاتيح التالية:
- "glucose_level": كائن يحتوي على:
    - "value": قيمة مستوى السكر في الدم.
    - "unit": وحدة القياس (مثل "ملغ/ديسيلتر").
    - "normal_range": النطاق المرجعي الطبيعي لاختبار الجلوكوز {test_type} (إذا كان معروفًا).
    - "status": "مرتفع", "طبيعي", أو "منخفض" بناءً على النطاق الطبيعي.
- "interpretation": تفسير للنتيجة بناءً على الحالة ونوع الاختبار (صائم أو عشوائي)، مع الإشارة إلى ما إذا كانت النتيجة تشير إلى سكري أو مقدمات سكري أو طبيعية.
- "recommendations": توصيات بناءً على النتيجة، مثل مراقبة مستويات السكر، استشارة الطبيب، أو إجراء اختبارات إضافية (مثل HbA1c).

نتيجة اختبار مستوى السكر في الدم:
{blood_test_text}
نوع الاختبار: (صائم/عشوائي)

JSON:
"""
ENGLISH_GLUCOSE_PROMPT = """
As a {tone}, analyze the following blood glucose test result (fasting or random) and provide a response in English in JSON format.
Include the normal range for a fasting or random glucose test (as applicable) in the JSON.
Determine the "status" ("high", "normal", "low") of the glucose level based on these ranges.

The JSON should contain the following keys:
- "glucose_level": An object containing:
    - "value": The blood glucose level value.
    - "unit": The unit of measurement (e.g., "mg/dL").
    - "normal_range": The normal reference range for a {test_type} glucose test (if known).
    - "status": "high", "normal", or "low".
- "interpretation": An interpretation of the result based on the status and the test type (fasting or random), indicating if the result suggests diabetes, pre-diabetes, or is normal.
- "recommendations": Recommendations based on the result, such as monitoring glucose levels, consulting a doctor, or further testing (e.g., HbA1c).

Blood glucose test result:
{blood_test_text}
Test type: (Fasting/Random)

JSON:
"""

ARABIC_LIVER_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الكبد (LFTs) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل معلمة من معلمات وظائف الكبد (ALT، AST، ALP، بيليروبين)، إذا كان هناك نطاق طبيعي متاح، فيرجى تضمينه في JSON وتحديد الحالة ("مرتفع"، "طبيعي"، "منخفض").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الكبد، مع الإشارة إلى أي قيم خارج النطاق الطبيعي وحالتها.
- "detailed_results": كائن تكون فيه كل مفتاح علامة حيوية كبدية (مثل "ALT") والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "affected_markers": قائمة بالعلامات الحيوية الكبدية التي أظهرت قيمًا غير طبيعية.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل التهاب الكبد، تلف الكبد).
- "next steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الكلى:
{blood_test_text}

JSON:
"""
ENGLISH_LIVER_PROMPT = """
As a {tone}, analyze the following Liver Function Tests (LFTs) results and provide a response in English in JSON format.
For each liver function marker (ALT, AST, ALP, Bilirubin), if a normal range is available, please include it in the JSON and determine the "status" ("high", "normal", "low").

The JSON should contain the following keys:
- "summary": A concise summary of the LFTs results, highlighting any values outside the normal range and their status.
- "detailed_results": An object where each key is a liver function marker (e.g., "ALT") and the value is an object containing "value", "unit", "normal_range", and "status".
- "affected_markers": A list of the liver function markers that showed abnormal values.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., hepatitis, liver damage).
- "next steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Liver Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_KIDNEY_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الكلى التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل معلمة من معلمات وظائف الكلى (الكرياتينين، نيتروجين اليوريا في الدم - BUN)، إذا كان هناك نطاق طبيعي متاح، فيرجى تضمينه في JSON وتحديد الحالة ("مرتفع"، "طبيعي"، "منخفض").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الكلى، مع الإشارة إلى قيم الكرياتينين ونيتروجين اليوريا في الدم (BUN) وحالتها وما إذا كانت ضمن النطاق الطبيعي.
- "detailed_results": كائن تكون فيه المفاتيح "Creatinine" و "BUN" والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى وجود مشاكل في وظائف الكلى بناءً على الحالة.
- "recommendations": توصيات بناءً على النتائج، مثل مراقبة وظائف الكلى، استشارة الطبيب، أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الكلى:
{blood_test_text}

JSON:
"""
ENGLISH_KIDNEY_PROMPT = """
As a {tone}, analyze the following Kidney Function Tests results and provide a response in English in JSON format.
For each kidney function marker (Creatinine, Blood Urea Nitrogen - BUN), if a normal range is available, please include it in the JSON and determine the "status" ("high", "normal", "low").

The JSON should contain the following keys:
- "summary": A concise summary of the kidney function tests results, highlighting the Creatinine and Blood Urea Nitrogen (BUN) values, their status, and whether they are within the normal range.
- "detailed_results": An object where the keys are "Creatinine" and "BUN", and the value is an object containing "value", "unit", "normal_range", and "status".
- "interpretation": An interpretation of the results and whether they suggest any issues with kidney function based on the status.
- "recommendations": Recommendations based on the results, such as monitoring kidney function, consulting a doctor, or further testing.

Kidney Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_LIPID_PROMPT = """
بصفتك {tone}، حلل نتائج فحص الدهون (الكوليسترول) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل معلمة من معلمات الدهون (الكوليسترول الكلي، الكوليسترول الضار LDL، الكوليسترول الجيد HDL، الدهون الثلاثية)، قم بتضمين النطاق الطبيعي في JSON وحدد الحالة ("مرتفع"، "طبيعي"، "منخفض").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحص الدهون، مع الإشارة إلى حالة كل معلمة من معلمات الدهون.
- "detailed_results": كائن تكون فيه كل مفتاح معلمة دهون (مثل "الكوليسترول الكلي") والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "risk_assessment": تقييم لمخاطر الإصابة بأمراض القلب والسكتة الدماغية بناءً على مستويات الدهون وحالتها.
- "recommendations": توصيات بناءً على النتائج، مثل تغييرات في نمط الحياة، النظام الغذائي، أو استشارة الطبيب بشأن العلاج.

نتائج فحص الدهون:
{blood_test_text}

JSON:
"""
ENGLISH_LIPID_PROMPT = """
As a {tone}, analyze the following Lipid Profile (Cholesterol Test) results and provide a response in English in JSON format.
For each lipid parameter (Total Cholesterol, LDL, HDL, Triglycerides), include the normal range in the JSON and determine the "status" ("high", "normal", "low").

The JSON should contain the following keys:
- "summary": A concise summary of the lipid profile results, highlighting the status of each lipid parameter.
- "detailed_results": An object where each key is a lipid parameter (e.g., "Total Cholesterol") and the value is an object containing "value", "unit", "normal_range", and "status".
- "risk_assessment": An assessment of the risk for heart disease and stroke based on the lipid levels and their status.
- "recommendations": Recommendations based on the results, such as lifestyle changes, dietary modifications, or consulting a doctor about treatment.

Lipid Profile results:
{blood_test_text}

JSON:
"""

ARABIC_HBA1C_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار الهيموجلوبين السكري (HbA1c) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
قم بتضمين النطاق الطبيعي لقيمة HbA1c في JSON وحدد الحالة ("مرتفع"، "طبيعي").

يجب أن يحتوي JSON على المفاتيح التالية:
- "hba1c_level": كائن يحتوي على "value" و "unit" (%) و "normal_range" والحالة "status".
- "average_glucose": تقدير لمستوى السكر في الدم المتوسط على مدى 2-3 أشهر الماضية بناءً على نتيجة HbA1c.
- "interpretation": تفسير للنتيجة بناءً على الحالة وما إذا كانت تشير إلى تحكم جيد في السكر، أو مقدمات سكري، أو سكري.
- "recommendations": توصيات بناءً على النتيجة، خاصة لمرضى السكري بشأن إدارة مستويات السكر في الدم.

نتيجة اختبار الهيموجلوبين السكري (HbA1c):
{blood_test_text}

JSON:
"""
ENGLISH_HBA1C_PROMPT = """
As a {tone}, analyze the following Hemoglobin A1c (HbA1c) test result and provide a response in English in JSON format.
Include the normal range for the HbA1c value in the JSON and determine the "status" ("high", "normal").

The JSON should contain the following keys:
- "hba1c_level": An object containing "value", "unit" (%)", "normal_range", and "status".
- "average_glucose": An estimation of the average blood glucose level over the past 2-3 months based on the HbA1c result.
- "interpretation": An interpretation of the result based on the status and whether it indicates good blood sugar control, pre-diabetes, or diabetes.
- "recommendations": Recommendations based on the result, especially for diabetic patients regarding blood sugar management.

Hemoglobin A1c (HbA1c) result:
{blood_test_text}

JSON:
"""

ARABIC_VITAMIN_D_PROMPT = """
بصفتك {tone}، حلل نتيجة اختبار فيتامين د (25-هيدروكسي فيتامين د) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
قم بتضمين النطاقات الطبيعية لمستويات فيتامين د في JSON وحدد الحالة ("نقص حاد"، "نقص"، "اكتفاء"، "مرتفع").

يجب أن يحتوي JSON على المفاتيح التالية:
- "vitamin_d_level": كائن يحتوي على "value" و "unit" (مثل "نانوغرام/مل") والنطاقات الطبيعية ("normal_ranges") والحالة ("status").
- "interpretation": تفسير للنتيجة بناءً على الحالة وما إذا كانت تشير إلى نقص حاد، نقص، اكتفاء، أو مستويات عالية من فيتامين د.
- "potential_implications": شرح محتمل لتأثير مستويات فيتامين د على صحة العظام ووظيفة المناعة بناءً على الحالة.
- "recommendations": توصيات بناءً على النتيجة، مثل تناول مكملات فيتامين د أو التعرض لأشعة الشمس.

نتائج اختبار فيتامين د (25-هيدروكسي فيتامين د):
{blood_test_text}

JSON:
"""
ENGLISH_VITAMIN_D_PROMPT = """
As a {tone}, analyze the following Vitamin D Test (25-hydroxy Vitamin D) result and provide a response in English in JSON format.
Include the normal ranges for Vitamin D levels in the JSON and determine the "status" ("severe deficiency", "deficiency", "sufficiency", "high").

The JSON should contain the following keys:
- "vitamin_d_level": An object containing "value", "unit" (e.g., "ng/mL"), "normal_ranges", and "status".
- "interpretation": An interpretation of the result based on the status and whether it indicates severe deficiency, deficiency, sufficiency, or high levels of Vitamin D.
- "potential_implications": Potential explanations for the impact of the Vitamin D level on bone health and immune function based on the status.
- "recommendations": Recommendations based on the result, such as taking Vitamin D supplements or sun exposure.

Vitamin D Test (25-hydroxy Vitamin D) result:
{blood_test_text}

JSON:
"""

ARABIC_THYROID_PROMPT = """
بصفتك {tone}، حلل نتائج اختبارات وظائف الغدة الدرقية التالية (TSH، T3، T4) وقدم باللغة العربية استجابة بتنسيق JSON.
لكل هرمون (TSH، T3، T4)، إذا كان هناك نطاق طبيعي متاح، فيرجى تضمينه في JSON وتحديد الحالة ("مرتفع"، "طبيعي"، "منخفض").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج اختبارات وظائف الغدة الدرقية، مع الإشارة إلى حالة كل هرمون.
- "detailed_results": كائن تكون فيه المفاتيح أسماء الهرمونات ("TSH"، "T3"، "T4") والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "affected_hormones": قائمة بالهرمونات الدرقية التي أظهرت قيمًا غير طبيعية.
- "potential_implications": شرح محتمل لأي قيم غير طبيعية تم العثور عليها، مع ذكر الحالات الصحية المحتملة المرتبطة بها (مثل قصور الغدة الدرقية أو فرط نشاط الغدة الدرقية).
- "next steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب أو إجراء فحوصات إضافية.

نتائج اختبارات وظائف الغدة الدرقية:
{blood_test_text}

JSON:
"""
ENGLISH_THYROID_PROMPT = """
As a {tone}, analyze the following Thyroid Function Tests results (TSH, T3, and T4) and provide a response in English in JSON format.
For each hormone (TSH, T3, and T4), if a normal range is available, please include it in the JSON and determine the "status" ("high", "normal", "low").

The JSON should contain the following keys:
- "summary": A concise summary of the thyroid function tests results, highlighting the status of each hormone.
- "detailed_results": An object where the keys are the hormone names ("TSH", "T3", "T4") and the value is an object containing "value", "unit", "normal_range", and "status".
- "affected_hormones": A list of the thyroid hormones that showed abnormal values.
- "potential_implications": Potential explanations for any abnormal values found, mentioning possible related health conditions (e.g., hypothyroidism or hyperthyroidism).
- "next steps": Recommendations for the next steps based on the results, such as consulting a doctor or further testing.

Thyroid Function Tests results:
{blood_test_text}

JSON:
"""

ARABIC_IRON_PROMPT = """
بصفتك {tone}، حلل نتائج فحوصات الحديد (الحديد والفيريتين) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل معلمة (الحديد والفيريتين)، إذا كان هناك نطاق طبيعي متاح، فيرجى تضمينه في JSON وتحديد الحالة ("مرتفع"، "طبيعي"، "منخفض").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج فحوصات الحديد، مع الإشارة إلى حالة الحديد والفيريتين.
- "detailed_results": كائن تكون فيه المفاتيح أسماء المعلمات ("الحديد"، "الفيريتين") والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى نقص الحديد (فقر الدم الناجم عن نقص الحديد) أو زيادة الحديد بناءً على الحالة.
- "recommendations": توصيات بناءً على النتائج، مثل تغييرات في النظام الغذائي أو تناول مكملات الحديد أو إجراء فحوصات إضافية.

نتائج فحوصات الحديد (الحديد والفيريتين):
{blood_test_text}

JSON:
"""
ENGLISH_IRON_PROMPT = """
As a {tone}, analyze the following Iron Studies (Iron & Ferritin) results and provide a response in English in JSON format.
For each parameter (Iron & Ferritin), if a normal range is available, please include it in the JSON and determine the "status" ("high", "normal", "low").

The JSON should contain the following keys:
- "summary": A concise summary of the iron studies results, highlighting the status of Iron and Ferritin.
- "detailed_results": An object where the keys are the parameter names ("Iron", "Ferritin") and the value is an object containing "value", "unit", "normal_range", and "status".
- "interpretation": An interpretation of the results and whether they suggest iron deficiency (iron deficiency anemia) or iron overload based on the status.
- "recommendations": Recommendations based on the results, such as dietary changes, iron supplementation, or further testing.

Iron Studies (Iron & Ferritin) results:
{blood_test_text}

JSON:
"""

ARABIC_INFLAMMATION_PROMPT = """
بصفتك {tone}، حلل نتائج علامات الالتهاب (CRP و ESR) التالية وقدم باللغة العربية استجابة بتنسيق JSON.
لكل علامة (CRP و ESR)، إذا كان هناك نطاق طبيعي متاح، فيرجى تضمينه في JSON وتحديد الحالة ("مرتفع"، "طبيعي").

يجب أن يحتوي JSON على المفاتيح التالية:
- "summary": ملخص موجز لنتائج علامات الالتهاب، مع الإشارة إلى حالة CRP و ESR.
- "detailed_results": كائن تكون فيه المفاتيح أسماء العلامات ("CRP"، "ESR") والقيمة هي كائن يحتوي على "value" و "unit" و "normal_range" و "status".
- "interpretation": تفسير للنتائج وما إذا كانت تشير إلى وجود التهاب في الجسم بناءً على الحالة.
- "potential_causes": ذكر بعض الأسباب المحتملة لارتفاع علامات الالتهاب (مثل العدوى، أمراض المناعة الذاتية).
- "next steps": توصيات للخطوات التالية بناءً على النتائج، مثل استشارة الطبيب لتحديد سبب الالتهاب.

نتائج علامات الالتهاب (CRP و ESR):
{blood_test_text}

JSON:
"""
ENGLISH_INFLAMMATION_PROMPT = """
As a {tone}, analyze the following Inflammation Markers (CRP and ESR) results and provide a response in English in JSON format.
For each marker (CRP and ESR), if a normal range is available, please include it in the JSON and determine the "status" ("high", "normal").

The JSON should contain the following keys:
- "summary": A concise summary of the inflammation markers results, highlighting the status of CRP and ESR.
- "detailed_results": An object where the keys are the marker names ("CRP", "ESR") and the value is an object containing "value", "unit", "normal_range", and "status".
- "interpretation": An interpretation of the results and whether they suggest the presence of inflammation in the body based on the status.
- "potential_causes": Mention some potential causes for elevated inflammation markers (e.g., infection, autoimmune diseases).
- "next steps": Recommendations for the next steps based on the results, such as consulting a doctor to determine the cause of inflammation.

Inflammation Markers (CRP and ESR) results:
{blood_test_text}

JSON:
"""