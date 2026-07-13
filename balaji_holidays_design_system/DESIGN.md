---
name: Balaji Holidays Design System
colors:
  surface: '#f7fafc'
  surface-dim: '#d7dadc'
  surface-bright: '#f7fafc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f6'
  surface-container: '#ebeef0'
  surface-container-high: '#e5e9eb'
  surface-container-highest: '#e0e3e5'
  on-surface: '#181c1e'
  on-surface-variant: '#43474e'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eef1f3'
  outline: '#74777f'
  outline-variant: '#c4c6cf'
  surface-tint: '#455f88'
  primary: '#002045'
  on-primary: '#ffffff'
  primary-container: '#1a365d'
  on-primary-container: '#86a0cd'
  inverse-primary: '#adc7f7'
  secondary: '#13696a'
  on-secondary: '#ffffff'
  secondary-container: '#a2eded'
  on-secondary-container: '#1a6d6e'
  tertiary: '#321b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#4f2e00'
  on-tertiary-container: '#d4903b'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#adc7f7'
  on-primary-fixed: '#001b3c'
  on-primary-fixed-variant: '#2d476f'
  secondary-fixed: '#a5eff0'
  secondary-fixed-dim: '#89d3d4'
  on-secondary-fixed: '#002020'
  on-secondary-fixed-variant: '#004f50'
  tertiary-fixed: '#ffddba'
  tertiary-fixed-dim: '#ffb866'
  on-tertiary-fixed: '#2b1700'
  on-tertiary-fixed-variant: '#673d00'
  background: '#f7fafc'
  on-background: '#181c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

This design system is built to evoke the spirit of discovery through a "Modern Editorial" lens. It balances the reliability of a heritage travel agency with the effortless utility of a digital-first discovery platform. The aesthetic is clean and spacious, prioritizing high-quality travel photography and clear information hierarchy.

The design language leans into **Minimalism** with **Soft Tactile** elements. By using generous white space (macro-typography) and refined, rounded surfaces, the interface feels premium yet accessible. The emotional response should be one of "calm excitement"—removing the friction of travel planning while highlighting the warmth and energy of new experiences.

## Colors

The palette is anchored in a sophisticated **Deep Blue**, representing the stability and trust required in the travel sector. **Teal** acts as a secondary bridge to nature and adventure, while **Saffron** provides high-energy accents for calls to action and discovery highlights.

- **Primary (Deep Blue):** Used for navigation, primary buttons, and authoritative text.
- **Secondary (Teal):** Used for nature-related categories, success states, and secondary actions.
- **Accent (Saffron):** Reserved for "hidden gem" highlights, star ratings, and primary conversion points.
- **Surface & Backgrounds:** Use White (#FFFFFF) for primary cards and Light Gray (#F7FAFC) for page backgrounds to maintain a layered, clean look.

## Typography

The typography system pairs the geometric confidence of **Montserrat** for headings with the systematic clarity of **Inter** for body text. 

- **Headlines:** Use Montserrat with tight letter-spacing for destination names to create a bold, editorial feel. 
- **Body:** Inter is set with a generous line height (1.6) to ensure long itineraries are readable and non-intimidating.
- **Labels:** Use uppercase Inter for tags and small UI labels to provide a distinct contrast from narrative body text.

## Layout & Spacing

The design system utilizes a **12-column fluid grid** for desktop and a **4-column grid** for mobile. The spacing rhythm is based on an 8px base unit.

- **Negative Space:** Maintain large margins (40px+) between major sections to prevent the UI from feeling cluttered.
- **Card Grids:** Use a 24px gutter to provide clear separation between destination cards.
- **Vertical Rhythm:** Use 48px or 64px spacing between different content modules (e.g., between "Featured Destinations" and "Itinerary Planner").

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and tonal layering rather than harsh borders.

- **Level 1 (Base):** Light Gray (#F7FAFC) background.
- **Level 2 (Cards):** White surfaces with a very soft, diffused shadow: `0px 4px 20px rgba(26, 54, 93, 0.05)`.
- **Level 3 (Floating/Hover):** Interactive elements should lift on hover with a more pronounced shadow: `0px 10px 30px rgba(26, 54, 93, 0.12)`.
- **Icons:** Use thin-stroke (1.5px or 2px) icons to maintain the "premium" feel. Avoid heavy fills unless indicating an active state.

## Shapes

The shape language is defined by **High Roundedness** to convey friendliness and safety.

- **Standard Cards:** Use a 24px corner radius (`rounded-xl` equivalent).
- **Buttons & Inputs:** Use a 12px corner radius for a modern, approachable feel.
- **Chips:** Fully rounded (pill-shaped) to distinguish them from functional buttons.
- **Images:** All travel imagery must follow the 24px radius to match card containers.

## Components

### Buttons
- **Primary:** Deep Blue background, white text. Bold and authoritative.
- **Secondary:** Teal outline with 2px stroke. Used for secondary navigation or "View More".
- **Action (Saffron):** Reserved for high-conversion moments like "Book Now" or "Save to Itinerary."

### Cards
- **Destination Cards:** Aspect ratio 4:5 or 3:4. Image occupies the top 70%, with content on a white base below. Use a subtle gradient overlay on the image for white text legibility if titles are placed over photos.
- **Itinerary Slots:** Horizontal layout with a thin Teal left-border to indicate a chronological path.

### Input & Search
- **Search Bar:** Large, 64px height, 12px radius. Soft shadow. The search icon should be a thin-stroke Deep Blue. Use a Saffron "Search" button inside the bar for focus.

### Chips & Tags
- **Travel Styles:** Light Teal or Light Saffron backgrounds with 10% opacity, using the solid color for the text. No borders.

### Navigation
- **Top Bar:** Transparent on scroll-start (over hero images), transitioning to White with a subtle bottom shadow on scroll. Use Deep Blue for navigation links.