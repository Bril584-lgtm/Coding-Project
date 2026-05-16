import random

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("The harder I work, the luckier I get.", "Gary Player"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("What you get by achieving your goals is not as important as what you become.", "Zig Ziglar"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Hardships often prepare ordinary people for an extraordinary destiny.", "C.S. Lewis"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
    ("Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.", "Roy T. Bennett"),
    ("I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Your limitation—it's only your imagination.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
    ("Do something today that your future self will thank you for.", "Unknown"),
]


def get_random_quote() -> tuple[str, str]:
    return random.choice(QUOTES)


def get_quote_by_index(index: int) -> tuple[str, str]:
    return QUOTES[index % len(QUOTES)]
