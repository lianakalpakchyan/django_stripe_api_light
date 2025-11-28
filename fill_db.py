import sqlite3 as sq

def fill_database():

    try:
        conn = sq.connect('db.sqlite3')
        cur = conn.cursor()

        items_query = """
        INSERT INTO items_item (name, description, price, currency)
        VALUES (?, ?, ?, ?)
        """

        items = [
            (
                'Aurora Ceramic Mug',
                'A handcrafted ceramic mug inspired by northern lights. Designed with a smooth matte finish and a '
                'comfortable rounded handle, perfect for morning coffee or evening tea. Each piece is slightly unique '
                'due to artisanal glazing techniques.',
                14.99,
                'USD'
            ),
            (
                'Lunar Desk Lamp',
                'A minimalist lamp shaped like a crescent moon, providing soft ambient light for reading or studying. '
                'The lamp uses energy-efficient LEDs and features adjustable brightness settings for personalized comfort.',
                39.50,
                'USD'
            ),
            (
                'Evergreen Journal',
                'A hardcover journal made from recycled paper with a forest-green fabric cover. Ideal for writing, '
                'drawing, note-taking, or organizing daily tasks. The pages are thick, smooth, and fountain-pen friendly.',
                11.25,
                'USD'
            ),
            (
                'Nebula Wall Poster',
                'A high-resolution space-themed poster depicting a colorful nebula captured by a deep-space telescope. '
                'Printed on premium matte paper that resists glare and fading, making it great for bedrooms or creative workspaces.',
                9.99,
                'USD'
            ),
            (
                'Cozy Knit Blanket',
                'A soft, oversized knit blanket woven using hypoallergenic yarn. Perfect for reading sessions, movie '
                'nights, or colder evenings. It adds texture and warmth to any living room or bedroom decor.',
                45.00,
                'USD'
            ),
            (
                'Stellar Bluetooth Speaker',
                'A portable Bluetooth speaker with crisp, balanced sound and a durable water-resistant exterior. Runs '
                'up to 15 hours on a single charge and supports hands-free calls through an integrated microphone.',
                59.00,
                'USD'
            ),
            (
                'Forest Pine Candle',
                'A long-burning soy candle infused with natural pine, cedarwood, and a hint of eucalyptus. Creates a '
                'refreshing woodland aroma that helps relax and clear the mind.',
                12.49,
                'USD'
            ),
            (
                'Vintage Leather Wallet',
                'A compact leather wallet handmade from full-grain Italian leather. Features multiple card slots, a '
                'secure coin pocket, and minimalistic stitching that gives it a classic, timeless appearance.',
                28.75,
                'EUR'
            ),
            (
                'Marble Phone Stand',
                'A polished natural-marble phone stand designed to securely hold any smartphone at a comfortable viewing '
                'angle. Adds elegance to desks, nightstands, or workspaces.',
                18.25,
                'EUR'
            ),
            (
                'Ocean Breeze Diffuser',
                'An essential-oil diffuser that releases a refreshing ocean-inspired scent. Uses silent ultrasonic technology '
                'and includes a soft blue night-light mode for relaxing environments.',
                22.80,
                'USD'
            ),
            (
                'Crimson Backpack',
                'A durable everyday backpack with multiple compartments, padded straps, and a laptop sleeve. Designed '
                'for students, commuters, and travelers who need both comfort and organization.',
                34.99,
                'USD'
            ),
            (
                'Solar-Charge Power Bank',
                'A rugged portable power bank that recharges using both sunlight and USB. Ideal for camping, long trips, '
                'or emergency situations when regular charging is not available.',
                29.50,
                'USD'
            ),
            (
                'Midnight Black Headphones',
                'Over-ear headphones delivering deep bass and clean treble. Features noise-isolating ear cushions and a '
                'foldable design for easy transport.',
                49.90,
                'USD'
            ),
            (
                'Rustic Wooden Clock',
                'A handcrafted wooden wall clock with engraved hour markings and a silent quartz mechanism. Perfect for '
                'kitchens, offices, or vintage-styled rooms.',
                26.00,
                'EUR'
            ),
            (
                'Cotton Cloud Pillow',
                'An ultra-soft pillow made from breathable cotton and filled with lightweight microfiber. Designed to '
                'maintain its shape and provide comfortable support for all sleep positions.',
                19.40,
                'USD'
            ),
            (
                'Glacier Sports Bottle',
                'A stainless-steel insulated bottle that keeps drinks cold for 24 hours or hot for 12 hours. Features a '
                'leak-proof lid and a powder-coated exterior for a secure grip.',
                17.90,
                'EUR'
            ),
        ]

        cur.executemany(items_query, items)

        discount_query = """
        INSERT INTO items_discount (percent_off)
        VALUES (?)
        """

        discount_values = [
            (0.00,),
            (5.00,),
            (10.00,),
            (15.00,),
            (20.00,),
            (25.00,),
            (30.00,),
            (35.00,),
            (40.00,),
            (45.00,),
            (50.00,),
        ]

        cur.executemany(discount_query, discount_values)

        tax_query = """
        INSERT INTO items_tax (display_name, inclusive, percentage)
        VALUES (?, ?, ?)
        """

        tax_values = [
            ('Zero VAT', False, 0.00),
            ('Standard VAT', False, 20.00),
            ('Reduced VAT', False, 10.00),
            ('Luxury Goods Tax', False, 28.50),
            ('Food Tax', True, 5.00),
            ('Medicine Tax', True, 2.50),
            ('Import Duty', False, 15.75),
            ('Environmental Tax', False, 3.25),
            ('Service Tax', False, 12.00),
            ('Digital Services Tax', False, 18.00),
            ('Hotel Accommodation Tax', True, 7.00),
            ('Restaurant Tax', True, 8.50),
            ('Tourism Tax', False, 6.00),
            ('Alcohol Tax', False, 25.00),
            ('Tobacco Tax', False, 30.00),
            ('Gaming Tax', False, 22.00),
            ('Transport Tax', False, 9.50),
            ('Construction Tax', False, 11.75),
            ('Agriculture Tax', True, 4.25),
            ('Energy Tax', False, 13.60),
        ]

        cur.executemany(tax_query, tax_values)

        conn.commit()
        print("Database filled successfully.")

    except Exception as e:
        print(f"Error filling database: {e}")
    finally:
        if 'conn' in locals() and conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    fill_database()
