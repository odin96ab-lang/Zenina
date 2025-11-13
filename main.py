import sqlite3
import telebot
from telebot import types
import logging
import time
from datetime import datetime, date

# إعدادات البوت
bot = telebot.TeleBot("8179581600:AAEIxHXruoCH_7eKinGe9zgXHsg25zyFdGk")

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)

# آيدي المطور
DEVELOPER_CHAT_ID = "6647899340"

# 🔢 نظام الإحصائيات المتكامل
def init_stats_db():
    try:
        conn = sqlite3.connect('bot_stats.db', check_same_thread=False)
        c = conn.cursor()
        
        # جدول المستخدمين
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                     username TEXT,
                     first_name TEXT,
                     last_name TEXT,
                     first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     message_count INTEGER DEFAULT 0)''')
        
        # جدول الإحصائيات اليومية
        c.execute('''CREATE TABLE IF NOT EXISTS daily_stats
                    (date TEXT PRIMARY KEY,
                     new_users INTEGER DEFAULT 0,
                     active_users INTEGER DEFAULT 0,
                     total_messages INTEGER DEFAULT 0)''')
        
        conn.commit()
        conn.close()
        print("✅ تم إنشاء قاعدة بيانات الإحصائيات")
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")

# تحديث إحصائيات المستخدم
def update_user_stats(user_id, username, first_name, last_name):
    try:
        conn = sqlite3.connect('bot_stats.db', check_same_thread=False)
        c = conn.cursor()
        
        # التحقق إذا كان المستخدم موجوداً
        c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        user_exists = c.fetchone()
        
        today = date.today().isoformat()
        
        if user_exists:
            # تحديث المستخدم الحالي
            c.execute('''UPDATE users 
                        SET username = ?, first_name = ?, last_name = ?, last_active = CURRENT_TIMESTAMP,
                        message_count = message_count + 1 
                        WHERE user_id = ?''',
                     (username, first_name, last_name, user_id))
            
            # تحديث الإحصائيات اليومية
            c.execute('''UPDATE daily_stats 
                        SET active_users = active_users + 1, total_messages = total_messages + 1
                        WHERE date = ?''', (today,))
            
        else:
            # إضافة مستخدم جديد
            c.execute('''INSERT INTO users (user_id, username, first_name, last_name, message_count)
                        VALUES (?, ?, ?, ?, 1)''',
                     (user_id, username, first_name, last_name))
            
            # تحديث الإحصائيات اليومية
            c.execute('''INSERT OR REPLACE INTO daily_stats (date, new_users, active_users, total_messages)
                        VALUES (?, 1, 1, 1)''', (today,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ خطأ في تحديث الإحصائيات: {e}")
        return False

# الحصول على الإحصائيات
def get_stats():
    try:
        conn = sqlite3.connect('bot_stats.db', check_same_thread=False)
        c = conn.cursor()
        
        # إجمالي المستخدمين
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        # المستخدمين النشطين اليوم
        today = date.today().isoformat()
        c.execute("SELECT active_users FROM daily_stats WHERE date = ?", (today,))
        result = c.fetchone()
        active_today = result[0] if result else 0
        
        # المستخدمين الجدد اليوم
        c.execute("SELECT new_users FROM daily_stats WHERE date = ?", (today,))
        result = c.fetchone()
        new_today = result[0] if result else 0
        
        # إجمالي الرسائل
        c.execute("SELECT SUM(message_count) FROM users")
        total_messages = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_today': active_today,
            'new_today': new_today,
            'total_messages': total_messages
        }
    except Exception as e:
        print(f"❌ خطأ في الحصول على الإحصائيات: {e}")
        return {'total_users': 0, 'active_today': 0, 'new_today': 0, 'total_messages': 0}

# تهيئة قاعدة البيانات الإحصائيات
init_stats_db()

# البيانات مباشرة في الكود بدون قاعدة بيانات
FAMILIES_DATA = {
    "العبد": {
        "branch": "أولاد سيدي أمحمد بن صالح",
        "sub_families": "ضيف الله، قدوري، خالدي، طاهري، ميلودي، عيساوي، دوامة",
        "genealogy": "عبد الله → بن قدور → بن محمد → بن علي → بن عبد الله → بن عيسى → بن الطيب → بن المسعود → بن بوزيان → بن قسمية → بن بوكثير → بن حامد → بن ضيف الله → بن زيان → بن سيدي أمحمد بن صالح",
        "history": "من أقدم وأعرق العائلات في المنطقة، تمتاز بتاريخ مشرف وحضور قوي في الحياة الاجتماعية والسياسية",
        "notable_members": "الشيخ طاهري، الشيخ خالدي مخلوف"
    },
    "أولاد الطيب بن سليمان": {
        "branch": "أولاد سيدي أمحمد بن صالح", 
        "sub_families": "رابحي، ميناري، بن عودة، حنيشي، تومي، صالحي، بوزيان، عامر، يحيىوي، صافي، بن جلول، عز الدين، بوحفص، تريشي",
        "genealogy": "الطيب → بن سليمان → بن علي → بن سليمان → بن محمد → بن رابح → بن عبد الله → بن عبد القادر → بن أحمد → بن الطيب → بن سالم → بن دحمان → بن إبراهيم → بن سيدي أمحمد بن صالح",
        "history": "عائلة علمية ودينية عريقة، برز منها العديد من العلماء والفقهاء",
        "notable_members": "الشيخ رابحي، العالم الجليل بن جلول"
    },
    "الزواتنية": {
        "branch": "أولاد سيدي أمحمد بن صالح",
        "sub_families": "زيتوني، بن شولة، زوابلية، غلام، ميمون، بن شهرة، جيلاني، بوزيدي، قلولة، ديسي",
        "genealogy": "محمد → بن أحمد → بن علي → بن عبد القادر → بن أحمد → بن محمد → بن أحمد → بن علي → بن صالح → بن داود → بن سليمان → بن بوكثير → بن سيدي أمحمد بن صالح",
        "history": "عائلة تجارية وزراعية بارزة، ساهمت في تطوير الاقتصاد المحلي", 
        "notable_members": "التاجر الكبير بن شولة، الشيخ زيتوني"
    },
    "الجنادة": {
        "branch": "أولاد سيدي أمحمد بن صالح",
        "sub_families": "شوية، لحذاري، بلحوت، زيغم، تريكي، صدوقي، رويغي، سويداني، مبروكي، بن رقية",
        "genealogy": "محمد → بن مالك → بن عبد الله → بن يحيى → بن لخضر → بن عيسى → بن محمد → بن عبد الله → بن محمود → بن عيسى → بن المسعود → بن سيدي أمحمد بن صالح",
        "history": "عائلة محاربة اشتهرت بالشجاعة والقيادة، كان لها دور بارز في الدفاع عن المنطقة",
        "notable_members": "القائد زيغم، المجاهد الشجاع شوية"
    }
}

PERSONALITIES_DATA = [
    {
        "name": "سيدي أمحمد بن صالح",
        "title": "مؤسس المدينة وزعيمها الروحي", 
        "era": "القرن الثامن عشر الميلادي",
        "biography": "رجل صالح وعالم جليل، اشترى أرض المدينة بمائة بقرة من قبيلة البدارنة الأمازيغية. كان مشهوراً بالحكمة والعدل وحسن التعامل مع الناس.",
        "contributions": "تأسيس النواة الأولى للمدينة، نشر الأمن والاستقرار، بناء المساجد والزوايا، تعمير الأرض وإحيائها.",
        "legacy": "يعتبر الأب الروحي للمدينة، وترك إرثاً من القيم الإسلامية والأخلاقية التي مازالت موجودة حتى اليوم."
    },
    {
        "name": "الشيخ عبد القادر طاهري",
        "title": "عالم دين ومصلح اجتماعي",
        "era": "1906 - القرن العشرين", 
        "biography": "من كبار علماء المنطقة، أسس زاوية لتحفيظ القرآن وتدريس العلوم الشرعية. كان معروفاً بعلمه الغزير وأخلاقه الرفيعة.",
        "contributions": "تأسيس الزاوية التعليمية، تخريج جيل من العلماء، نشر العلم والمعرفة، الإصلاح بين الناس.",
        "legacy": "أحد رواد التعليم النظامي في المنطقة، ومؤسس نهضة علمية ودينية استفاد منها الكثيرون."
    },
    {
        "name": "الزيغم",
        "title": "قائد عسكري وإداري",
        "era": "العصر العثماني",
        "biography": "قائد عسكري بارز في العهد العثماني، عُرف بحسن الإدارة والعدل والاهتمام بالرعية.",
        "contributions": "بناء الحارة القديمة، غرس البساتين، تنظيم الشؤون الإدارية، حفظ الأمن في المنطقة.", 
        "legacy": "وضع الأسس العمرانية والإدارية للمدينة في العصر العثماني، وترك نظاماً إدارياً متكاملاً."
    }
]

EVENTS_DATA = [
    {
        "name": "الغزو الروماني للمنطقة",
        "year": "العصر الروماني",
        "description": "قام الرومان بغزو المنطقة وتركوا آثاراً واضحة في جبال سردون، حيث بنوا الحصون وتركوا النقوش والمقابر التي تشهد على وجودهم.",
        "impact": "ترك الرومان إرثاً معمارياً وتاريخياً مهماً ما زال مرئياً حتى اليوم في المقابر والنقوش الحجرية."
    },
    {
        "name": "دخول الإسلام إلى المنطقة", 
        "year": "القرن السابع الميلادي",
        "description": "دخل الإسلام المنطقة مع الفتوحات الإسلامية، واعتنقه السكان المحليون تدريجياً، وتحولت المنطقة إلى مركز إشعاع إسلامي.",
        "impact": "تحول جذري في الثقافة والمجتمع، ظهور المساجد والمدارس الإسلامية، انتشار الثقافة العربية الإسلامية."
    },
    {
        "name": "شراء الأرض وتأسيس المدينة",
        "year": "القرن الثامن عشر الميلادي", 
        "description": "اشترى سيدي أمحمد بن صالح الأرض من قبيلة البدارنة الأمازيغية بمائة بقرة، وبدأ في تعميرها وإنشاء المساجد والمنازل.",
        "impact": "تأسيس النواة الحضرية الأولى التي تطورت لتصبح مدينة الإدريسية، وبداية التاريخ الحديث للمدينة."
    }
]

LANDMARKS_DATA = [
    {
        "name": "جبال سردون",
        "type": "معلم طبيعي وأثري",
        "location": "غرب المدينة",
        "description": "سلسلة جبلية شاهقة تحتوي على مقابر رومانية ونقوش حجرية ومغارات طبيعية، اكتشفها الباحث ليرانس",
        "historical_importance": "شاهد حي على تعاقب الحضارات في المنطقة عبر العصور المختلفة"
    },
    {
        "name": "عين زنينة",
        "type": "معلم طبيعي",
        "location": "وسط المدينة التاريخي",
        "description": "منبع مياه طبيعي كان السبب الرئيسي في استقرار السكان وتأسيس القرية الأولى",
        "historical_importance": "مصدر الحياة والزراعة عبر القرون، وكان محور الحياة اليومية"
    },
    {
        "name": "الضاية المالحة",
        "type": "معلم طبيعي",
        "location": "14 كم غرب المدينة",
        "description": "بحيرة مالحة طبيعية تجذب الطيور المهاجرة، وتحتوي على بقايا قصور أثرية حولها",
        "historical_importance": "نظام بيئي فريد وشاهد على المناخ القديم للمنطقة"
    },
    {
        "name": "القصر القديم",
        "type": "معلم أثري",
        "location": "الحي التاريخي",
        "description": "أقدم قصر في المدينة، بني في العصر العثماني وكان مقراً للحكام المحليين",
        "historical_importance": "رمز للسيادة والتاريخ العمراني للمدينة"
    },
    {
        "name": "المسجد العتيق",
        "type": "معلم ديني",
        "location": "الحي القديم",
        "description": "أقدم مسجد في المدينة، بني عام 1891 وكان مركزاً للتعليم والعبادة",
        "historical_importance": "مركز ديني واجتماعي ورمز للهوية الإسلامية"
    }
]

# تخزين آخر رسالة لكل مستخدم
user_last_message = {}

# حالة المستخدم لتتبع ما يريد فعله
user_states = {}

# لوحة المفاتيح الرئيسية
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('🏛️ عن المدينة')
    btn2 = types.KeyboardButton('👑 العائلات')
    btn3 = types.KeyboardButton('⭐ الشخصيات') 
    btn4 = types.KeyboardButton('📅 الأحداث')
    btn5 = types.KeyboardButton('🗺️ الجغرافيا')
    btn6 = types.KeyboardButton('📖 التاريخ')
    btn7 = types.KeyboardButton('🏰 المعالم')
    btn8 = types.KeyboardButton('📞 الاتصال')
    btn9 = types.KeyboardButton('📊 الإحصائيات')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return markup

# إرسال رسالة مع الأزرار
def send_message_with_keyboard(chat_id, text, reply_markup=None):
    try:
        msg = bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='Markdown')
        user_last_message[chat_id] = msg.message_id
        return msg
    except Exception as e:
        print(f"❌ خطأ في إرسال الرسالة: {e}")

# تحديث الإحصائيات لكل رسالة (دالة مساعدة)
def update_stats_handler(message):
    try:
        user_id = message.chat.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        
        # تحديث الإحصائيات لكل رسالة
        update_user_stats(user_id, username, first_name, last_name)
    except Exception as e:
        print(f"❌ خطأ في تحديث الإحصائيات: {e}")

# أمر الإحصائيات
@bot.message_handler(func=lambda message: message.text == '📊 الإحصائيات')
def show_stats(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass
        
        stats = get_stats()
        
        stats_text = f"""
📊 **إحصائيات البوت الشاملة**

👥 **المستخدمين:**
• 🧮 الإجمالي: {stats['total_users']} مستخدم
• 🔥 النشطين اليوم: {stats['active_today']} مستخدم
• 🆕 الجدد اليوم: {stats['new_today']} مستخدم

💬 **الرسائل:**
• 📨 الإجمالي: {stats['total_messages']} رسالة

⏰ **آخر تحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 **البوت في تطور مستمر!**
        """
        
        send_message_with_keyboard(message.chat.id, stats_text, main_keyboard())
        print("✅ تم عرض الإحصائيات بنجاح")
        
    except Exception as e:
        error_msg = f"❌ حدث خطأ في عرض الإحصائيات: {str(e)}"
        send_message_with_keyboard(message.chat.id, error_msg, main_keyboard())
        print(f"❌ خطأ في الإحصائيات: {e}")

# أمر البدء
@bot.message_handler(commands=['start'])
def start(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة إذا كانت موجودة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        welcome_text = """
🏛️ **مرحباً بك في بوت مدينة الإدريسية (زنينة)**

*موسوعة شاملة عن تاريخ وتراث المدينة*

📚 **الأقسام المتاحة:**
• 🏛️ عن المدينة - معلومات أساسية
• 👑 العائلات - أنساب كاملة وتفصيلية  
• ⭐ الشخصيات - سير ذاتية للشخصيات البارزة
• 📅 الأحداث - أحداث تاريخية مفصلة
• 🗺️ الجغرافيا - موقع وطبيعة المدينة
• 📖 التاريخ - تاريخ شامل للمدينة
• 🏰 المعالم - المعالم التاريخية والأثرية
• 📞 الاتصال - التواصل مع المطور
• 📊 الإحصائيات - إحصائيات البوت

اختر القسم الذي تريد الاستكشاف 👇
        """
        send_message_with_keyboard(message.chat.id, welcome_text, main_keyboard())
        print("✅ تم استقبال أمر /start بنجاح")
    except Exception as e:
        print(f"❌ خطأ في start: {e}")

# 👑 العائلات
@bot.message_handler(func=lambda message: message.text == '👑 العائلات')
def show_families(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        intro_text = """
👑 **العائلات العريقة في الإدريسية (زنينة)**

تنحدر معظم العائلات الأصلية من السلالة الشريفة لسيدي أمحمد بن صالح

**اختر العائلة التي تريد معرفة المزيد عنها:**
        """
        msg = send_message_with_keyboard(message.chat.id, intro_text, families_keyboard())

    except Exception as e:
        error_msg = f"❌ حدث خطأ في عرض العائلات: {str(e)}"
        send_message_with_keyboard(message.chat.id, error_msg, main_keyboard())
        print(f"❌ خطأ في العائلات: {e}")

# لوحة مفاتيح العائلات
def families_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    buttons = []
    for family_name in FAMILIES_DATA.keys():
        buttons.append(types.KeyboardButton(f'👑 {family_name}'))
    buttons.append(types.KeyboardButton('🔙 الرجوع للقائمة الرئيسية'))
    markup.add(*buttons)
    return markup

# عرض عائلة محددة
@bot.message_handler(func=lambda message: message.text.startswith('👑 '))
def show_specific_family(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        family_name = message.text.replace('👑 ', '').strip()

        if family_name in FAMILIES_DATA:
            family_data = FAMILIES_DATA[family_name]

            family_text = f"""
**🏛️ عائلة {family_name}**

**🌿 الفرع:** {family_data['branch']}

**👥 الألقاب والعائلات:**
{family_data['sub_families']}

**📜 النسب الشريف:**
{family_data['genealogy']}

**📖 التاريخ والمكانة:**
{family_data['history']}

**⭐ أعلام العائلة:**
{family_data['notable_members']}
            """

            # حذف الرسالة السابقة
            if message.chat.id in user_last_message:
                try:
                    bot.delete_message(message.chat.id, user_last_message[message.chat.id])
                except:
                    pass

            send_message_with_keyboard(message.chat.id, family_text, families_keyboard())

        else:
            send_message_with_keyboard(message.chat.id, "❌ العائلة غير موجودة", families_keyboard())

    except Exception as e:
        print(f"❌ خطأ في عرض العائلة المحددة: {e}")

# ⭐ الشخصيات
@bot.message_handler(func=lambda message: message.text == '⭐ الشخصيات')
def show_personalities(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # إرسال كل شخصية بشكل منفصل مع تأخير بسيط
        intro_text = """
⭐ **الشخصيات البارزة في تاريخ الإدريسية (زنينة)**

أعلام ساهموا في بناء المدينة وتطويرها عبر العصور
        """
        msg = send_message_with_keyboard(message.chat.id, intro_text, main_keyboard())

        # تأخير بسيط بين الرسائل
        time.sleep(1)

        for person in PERSONALITIES_DATA:
            person_text = f"""
**👑 {person['name']}**
**🏷️ اللقب:** {person['title']}
**⏳ العصر:** {person['era']}

**📜 السيرة الذاتية:**
{person['biography']}

**🎯 الإسهامات:**
{person['contributions']}

**💫 الإرث والتأثير:**
{person['legacy']}
────────────────────
            """
            bot.send_message(message.chat.id, person_text, parse_mode='Markdown')
            time.sleep(0.5)

        print("✅ تم عرض الشخصيات بنجاح")
    except Exception as e:
        error_msg = f"❌ حدث خطأ في عرض الشخصيات: {str(e)}"
        send_message_with_keyboard(message.chat.id, error_msg, main_keyboard())
        print(f"❌ خطأ في الشخصيات: {e}")

# 📅 الأحداث
@bot.message_handler(func=lambda message: message.text == '📅 الأحداث')
def show_events(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # إرسال مقدمة مع الأزرار
        intro_text = """
📅 **الأحداث التاريخية المهمة في الإدريسية (زنينة)**

محطات شكلت وجه المدينة وتركت بصماتها على تاريخها
        """
        msg = send_message_with_keyboard(message.chat.id, intro_text, main_keyboard())

        # تأخير بسيط
        time.sleep(1)

        # إرسال الأحداث بشكل منفصل
        for event in EVENTS_DATA:
            event_text = f"""
**📅 {event['name']}**
**🗓️ التاريخ:** {event['year']}

**📖 وصف الحدث:**
{event['description']}

**⚡ التأثير والنتائج:**
{event['impact']}
────────────────────
            """
            bot.send_message(message.chat.id, event_text, parse_mode='Markdown')
            time.sleep(0.5)

        print("✅ تم عرض الأحداث بنجاح")
    except Exception as e:
        error_msg = f"❌ حدث خطأ في عرض الأحداث: {str(e)}"
        send_message_with_keyboard(message.chat.id, error_msg, main_keyboard())
        print(f"❌ خطأ في الأحداث: {e}")

# 🏰 المعالم التاريخية
@bot.message_handler(func=lambda message: message.text == '🏰 المعالم')
def show_landmarks(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # إرسال مقدمة مع الأزرار
        intro_text = """
🏰 **المعالم التاريخية والأثرية في الإدريسية (زنينة)**

شواهد حية على عراقة المدينة وتعدد الحضارات
        """
        msg = send_message_with_keyboard(message.chat.id, intro_text, main_keyboard())

        # تأخير بسيط
        time.sleep(1)

        # إرسال المعالم بشكل منفصل
        for landmark in LANDMARKS_DATA:
            landmark_text = f"""
**🏰 {landmark['name']}**
**📝 النوع:** {landmark['type']}
**📍 الموقع:** {landmark['location']}

**📖 الوصف:**
{landmark['description']}

**⭐ الأهمية التاريخية:**
{landmark['historical_importance']}
────────────────────
            """
            bot.send_message(message.chat.id, landmark_text, parse_mode='Markdown')
            time.sleep(0.5)

        print("✅ تم عرض المعالم بنجاح")
    except Exception as e:
        error_msg = f"❌ حدث خطأ في عرض المعالم: {str(e)}"
        send_message_with_keyboard(message.chat.id, error_msg, main_keyboard())
        print(f"❌ خطأ في المعالم: {e}")

# 📞 الاتصال بالمطور
@bot.message_handler(func=lambda message: message.text == '📞 الاتصال')
def contact_developer(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        contact_text = """
📞 **الاتصال بالمطور**

**اختر نوع التواصل:**

🛠️ **الإبلاغ عن خطأ:** للإبلاغ عن أخطاء في المعلومات
📝 **المساهمة بمعلومات:** لإضافة معلومات جديدة
🔙 **الرجوع:** للعودة للقائمة الرئيسية

اختر الخيار المناسب:
        """
        send_message_with_keyboard(message.chat.id, contact_text, contact_keyboard())
        print("✅ تم عرض معلومات الاتصال بنجاح")
    except Exception as e:
        print(f"❌ خطأ في عرض الاتصال: {e}")

# لوحة مفاتيح الاتصال
def contact_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('🛠️ الإبلاغ عن خطأ')
    btn2 = types.KeyboardButton('📝 المساهمة بمعلومات')
    btn3 = types.KeyboardButton('🔙 الرجوع للقائمة الرئيسية')
    markup.add(btn1, btn2, btn3)
    return markup

# معالجة الإبلاغ عن الأخطاء
@bot.message_handler(func=lambda message: message.text == '🛠️ الإبلاغ عن خطأ')
def report_error(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # حفظ حالة المستخدم
        user_states[message.chat.id] = 'reporting_error'

        error_text = """
🛠️ **الإبلاغ عن خطأ**

**الآن يمكنك إرسال رسالتك مباشرة:**

📋 **يرجى تضمين المعلومات التالية:**
1. القسم الذي يوجد فيه الخطأ (مثل: العائلات، الشخصيات، إلخ)
2. وصف الخطأ بالتفصيل
3. المعلومات الصحيحة إن كانت متوفرة

✍️ **اكتب رسالتك الآن وسيتم إرسالها للمطور...**

أو اضغط ❌ إلغاء للعودة
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('❌ إلغاء'))
        send_message_with_keyboard(message.chat.id, error_text, markup)

    except Exception as e:
        print(f"❌ خطأ في الإبلاغ عن الخطأ: {e}")

# معالجة المساهمة بالمعلومات
@bot.message_handler(func=lambda message: message.text == '📝 المساهمة بمعلومات')
def contribute_info(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # حفظ حالة المستخدم
        user_states[message.chat.id] = 'contributing_info'

        contribute_text = """
📝 **المساهمة بمعلومات**

**الآن يمكنك إرسال معلوماتك مباشرة:**

📚 **يمكنك المساهمة في:**
- معلومات جديدة عن العائلات
- شخصيات تاريخية إضافية  
- أحداث تاريخية مهمة
- معالم أثرية وتاريخية
- تصحيحات للمعلومات الحالية

📋 **نموذج مقترح:**
- نوع المعلومات: [عائلة/شخصية/حدث/معلم]
- العنوان: [اسم العائلة/الشخص/الحدث/المعلم]
- التفاصيل: [المعلومات الكاملة]

✍️ **اكتب رسالتك الآن وسيتم إرسالها للمطور...**

أو اضغط ❌ إلغاء للعودة
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('❌ إلغاء'))
        send_message_with_keyboard(message.chat.id, contribute_text, markup)

    except Exception as e:
        print(f"❌ خطأ في المساهمة بالمعلومات: {e}")

# معالجة الرسائل النصية من المستخدمين
@bot.message_handler(func=lambda message: message.chat.id in user_states and message.text != '❌ إلغاء')
def handle_user_messages(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        user_id = message.chat.id
        user_state = user_states.get(user_id)

        if user_state == 'reporting_error':
            # إرسال تقرير الخطأ للمطور
            report_message = f"""
🚨 **بلاغ عن خطأ جديد**

👤 من: {message.from_user.first_name} {message.from_user.last_name or ''}
🆔 ID: {user_id}
📅 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **الرسالة:**
{message.text}
            """

            try:
                bot.send_message(DEVELOPER_CHAT_ID, report_message, parse_mode='Markdown')
                # تأكيد للمستخدم
                bot.send_message(user_id, "✅ **تم إرسال بلاغك بنجاح للمطور**\n\nشكراً لك على مساهمتك في تحسين البوت! 🙏", reply_markup=main_keyboard())
            except Exception as e:
                print(f"❌ خطأ في إرسال الرسالة للمطور: {e}")
                bot.send_message(user_id, "📝 **تم حفظ رسالتك:**\n\n" + message.text + "\n\nسيتم مراجعتها قريباً. شكراً لك! 🙏", reply_markup=main_keyboard())

        elif user_state == 'contributing_info':
            # إرسال المساهمة للمطور
            contribution_message = f"""
🎯 **مساهمة جديدة بالمعلومات**

👤 من: {message.from_user.first_name} {message.from_user.last_name or ''}
🆔 ID: {user_id}  
📅 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **المساهمة:**
{message.text}
            """

            try:
                bot.send_message(DEVELOPER_CHAT_ID, contribution_message, parse_mode='Markdown')
                # تأكيد للمستخدم
                bot.send_message(user_id, "✅ **تم إرسال مساهمتك بنجاح للمطور**\n\nشكراً لك على إثراء محتوى البوت! 🌟", reply_markup=main_keyboard())
            except Exception as e:
                print(f"❌ خطأ في إرسال المساهمة للمطور: {e}")
                bot.send_message(user_id, "📝 **تم حفظ مساهمتك:**\n\n" + message.text + "\n\nسيتم مراجعتها قريباً. شكراً لك! 🌟", reply_markup=main_keyboard())

        # مسح حالة المستخدم
        user_states.pop(user_id, None)

    except Exception as e:
        print(f"❌ خطأ في معالجة رسالة المستخدم: {e}")
        bot.send_message(message.chat.id, "❌ حدث خطأ في إرسال رسالتك. حاول مرة أخرى.", reply_markup=main_keyboard())

# معالجة إلغاء الإجراء
@bot.message_handler(func=lambda message: message.text == '❌ إلغاء')
def cancel_action(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # مسح حالة المستخدم
        user_states.pop(message.chat.id, None)

        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        # العودة للقائمة الرئيسية
        start(message)

    except Exception as e:
        print(f"❌ خطأ في الإلغاء: {e}")

# 🏛️ عن المدينة
@bot.message_handler(func=lambda message: message.text == '🏛️ عن المدينة')
def about_city(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        about_text = """
🏛️ **مدينة الإدريسية (زنينة) - ولاية الجلفة**

**الموقع والجغرافيا:**
- تقع غرب ولاية الجلفة
- المساحة: 375 كم²
- السكان: 38,000 نسمة
- تحدها: من الشمال بلدية القديد، ومن الجنوب بلدية تعضميت والأغواط، ومن الغرب أفلو، ومن الشرق الشارف والجلفة
**التضاريس:**
- جبال سردون الشاهقة
- عين زنينة الطبيعية
- الضاية المالحة
- وديان خصبة

**الاقتصاد:**
- الزراعة وتربية الماشية
- صناعة الفخار التقليدية
- التجارة مع المدن المجاورة

**التاريخ:**
- تأسست في القرن 18 الميلادي
- مؤسسها: سيدي أمحمد بن صالح
- تاريخ غني بالحوادث والأحداث
        """
        send_message_with_keyboard(message.chat.id, about_text, main_keyboard())
        print("✅ تم عرض معلومات المدينة بنجاح")
    except Exception as e:
        print(f"❌ خطأ في عن المدينة: {e}")

# 📖 التاريخ
@bot.message_handler(func=lambda message: message.text == '📖 التاريخ')
def show_history(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        history_text = """
📖 **التاريخ الشامل للإدريسية (زنينة)**

**العصور القديمة:**
- آثار رومانية في جبال سردون
- طريق تجاري مهم بين المدن
- نقوش ومقابر تعود للحقبة الرومانية

**العصر الإسلامي:**
- دخول الإسلام في القرن 7 الميلادي
- انتشار الزوايا التعليمية
- تأسيس المساجد والمدارس

**الاحتلال الفرنسي:**
- وصول الفرنسيين 28 أبريل 1845
- بناء المدارس والمؤسسات
- مقاومة شرسة من السكان

**الثورة التحريرية:**
- مركز دعم للثوار
- معارك بطولية في جبال سردون
- تقديم الشهداء والمجاهدين

**ما بعد الاستقلال:**
- تطور الخدمات والتعليم
- ازدهار الزراعة والتجارة
- الحفاظ على التراث والتقاليد
        """
        send_message_with_keyboard(message.chat.id, history_text, main_keyboard())
        print("✅ تم عرض التاريخ بنجاح")
    except Exception as e:
        print(f"❌ خطأ في التاريخ: {e}")

# 🗺️ الجغرافيا
@bot.message_handler(func=lambda message: message.text == '🗺️ الجغرافيا')
def show_geography(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        geography_text = """
🗺️ **الجغرافيا والطبيعة في الإدريسية (زنينة)**

**التضاريس:**
- موقع استراتيجي يجمع بين السهول والجبال
- جبال سردون الأثرية (1400 متر)
- عين زنينة الطبيعية
- الضاية المالحة (14 كم غرب المدينة)

**الموارد الطبيعية:**
- مياه عذبة من العيون الطبيعية
- تربة خصبة للزراعة
- موارد طينية لصناعة الفخار
- ثروة حيوانية (الماشية)

**المناخ:**
- مناخ متوسطي متأثر بالصحراء
- أمطار موسمية (300-400 ملم سنوياً)
- صيف معتدل وشتاء بارد
- تنوع نباتي وحيواني
        """
        send_message_with_keyboard(message.chat.id, geography_text, main_keyboard())
        print("✅ تم عرض الجغرافيا بنجاح")
    except Exception as e:
        print(f"❌ خطأ في الجغرافيا: {e}")

# 🔙 الرجوع للقائمة الرئيسية
@bot.message_handler(func=lambda message: message.text == '🔙 الرجوع للقائمة الرئيسية')
def back_to_main(message):
    start(message)

# معالجة الرسائل الأخرى
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # تحديث الإحصائيات أولاً
        update_stats_handler(message)
        
        # حذف الرسالة السابقة
        if message.chat.id in user_last_message:
            try:
                bot.delete_message(message.chat.id, user_last_message[message.chat.id])
            except:
                pass

        send_message_with_keyboard(message.chat.id, "❌ لم أفهم طلبك. الرجاء استخدام الأزرار الموجودة في الأسفل.", main_keyboard())
    except Exception as e:
        print(f"❌ خطأ في معالجة الرسالة: {e}")

# تشغيل البوت
if __name__ == "__main__":
    print("🚀 بدأ تشغيل بوت مدينة الإدريسية...")
    print("📊 المحتوى المتاح:")
    print(f"   • 👑 {len(FAMILIES_DATA)} عائلة عريقة")
    print(f"   • ⭐ {len(PERSONALITIES_DATA)} شخصية بارزة") 
    print(f"   • 📅 {len(EVENTS_DATA)} حدث تاريخي")
    print(f"   • 🏰 {len(LANDMARKS_DATA)} معلم تاريخي")
    print(f"   • 📞 نظام اتصال مع المطور (آيدي: {DEVELOPER_CHAT_ID})")
    print("   • 📊 نظام إحصائيات متكامل")
    print("✅ البوت جاهز للاستخدام!")

    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")