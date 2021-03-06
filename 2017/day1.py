"""Advent of Code 2017 Day 1 Inverse Captcha"""
# The night before Christmas, one of Santa's Elves calls you in a panic.
# "The printer's broken! We can't print the Naughty or Nice List!" By the
# time you make it to sub-basement 17, there are only a few minutes until 
# midnight."We have a big problem," she says; "there must be almost fifty
# bugs in this system, but nothing else can print The List. Stand in this
# square, quick! There's no time to explain; if you can convince them to pay
# you in stars, you'll be able to--" She pulls a lever and the world goes
# blurry.
# 
# When your eyes can focus again, everything seems a lot more pixelated than
# before. She must have sent you inside the computer! You check the system
# clock: 25 milliseconds until midnight. With that much time, you should be
# able to collect all fifty stars by December 25th.
# 
# Collect stars by solving puzzles. Two puzzles will be made available on
# each day millisecond in the advent calendar; the second puzzle is unlocked
# when you complete the first. Each puzzle grants one star. Good luck!
# 
# You're standing in a room with "digitization quarantine" written in LEDs
# along one wall. The only door is locked, but it includes a small
# interface. "Restricted Area - Strictly No Digitized Users Allowed."
# 
# It goes on to explain that you may only leave by solving a captcha to
# prove you're not a human. Apparently, you only get one millisecond to
# solve the captcha: too fast for a normal human, but it feels like hours to
# you.
# 
# The captcha requires you to review a sequence of digits (your puzzle
# input) and find the sum of all digits that match the next digit in the
# list. The list is circular, so the digit after the last digit is the first
# digit in the list.
# 
# For example:
# - 1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the
# second digit and the third digit (2) matches the fourth digit.
# - 1111 produces 4 because each digit (all 1) matches the next.
# - 1234 produces 0 because no digit matches the next.
# - 91212129 produces 9 because the only digit that matches the next one is
# the last digit, 9.

def solve_part1(sequence):
    """Solve part 1 of the puzzle"""
    previous = None
    total = 0
    if len(sequence) >= 2:
        for digit in sequence:
            if digit == previous:
                total = total + int(digit)
            previous = digit
    
        if sequence[0] == previous:
            total = total + int(previous)
    
    print total

# --- Part Two ---
# 
# You notice a progress bar that jumps to 50% completion. Apparently, the
# door isn't yet satisfied, but it did emit a star as encouragement. The
# instructions change:
# 
# Now, instead of considering the next digit, it wants you to consider the
# digit halfway around the circular list. That is, if your list contains 10 items, only include a digit in your sum if the digit 10/2 = 5 steps
# forward matches it. Fortunately, your list has an even number of elements.
# 
# For example:
# 
# -1212 produces 6: the list contains 4 items, and all four digits match the
# digit 2 items ahead.
# -1221 produces 0, because every comparison is between a 1 and a 2.
# -123425 produces 4, because both 2s match each other, but no other digit
# has a match.
# -123123 produces 12.
# -12131415 produces 4.

def solve_part2(sequence):
    """Solve part 2 of the puzzle"""
    total = 0
    half = len(sequence) / 2
    for pos in range(half):
        if sequence[pos] == sequence[pos + half]:
            total = total + (int(sequence[pos]) * 2)
    print total

if __name__ == "__main__":
    INPUT = "57276274387944537823652626177853384411146325384494935924454336611953119173638191671326254832624841593421667683474349154668177743437745965461678636631863541462893547616877914914662358836365421198516263335926544716331814125295712581158399321372683742773423626286669759415959391374744214595682795818615532673877868424196926497731144319736445141728123322962547288572434564178492753681842244888368542423832228211172842456231275738182764232265933625119312598161192193214898949267765417468348935134618964683127194391796165368145548814473129857697989322621368744725685183346825333247866734735894493395218781464346951777873929898961358796274889826894529599645442657423438562423853247543621565468819799931598754753467593832328147439341586125262733737128386961596394728159719292787597426898945198788211417854662948358422729471312456437778978749753927251431677533575752312447488337156956217451965643454445329758327129966657189332824969141448538681979632611199385896965946849725421978137753366252459914913637858783146735469758716752765718189175583956476935185985918536318424248425426398158278111751711911227818826766177996223718837428972784328925743869885232266127727865267881592395643836999244218345184474613129823933659422223685422732186536199153988717455568523781673393698356967355875123554797755491181791593156433735591529495984256519631187849654633243225118132152549712643273819314433877592644693826861523243946998615722951182474773173215527598949553185313259992227879964482121769617218685394776778423378182462422788277997523913176326468957342296368178321958626168785578977414537368686438348124283789748775163821457641135163495649331144436157836647912852483177542224864952271874645274572426458614384917923623627532487625396914111582754953944965462576624728896917137599778828769958626788685374749661741223741834844643725486925886933118382649581481351844943368484853956759877215252766294896496444835264357169642341291412768946589781812493421379575569593678354241223363739129813633236996588711791919421574583924743119867622229659211793468744163297478952475933163259769578345894367855534294493613767564497137369969315192443795512585"     
    solve_part1(INPUT)
    solve_part2(INPUT)
