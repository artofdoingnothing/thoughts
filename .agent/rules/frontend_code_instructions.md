---
trigger: model_decision
description: When the frontend/client code is being worked on.
---

# Client Code Guidelines

## Technology Stack

- **Framework**: React
- **UI Library**: Material UI (MUI)
- **Styling**: Emotion (MUI default) or SCSS modules if necessary, but prefer MUI's `sx` prop or styled components.

## Color Palette

### CSS Variables

```css
:root {
  /* Text Colors */
  --text-primary: #1a1a1a;
  --text-secondary: #4a4a4a;
  --text-muted: #6b7280;
  --text-inverse: #ffffff;

  /* Blue Palette */
  --deep-blue: #1e3a8a;
  --medium-blue: #2563eb;
  --light-blue: #dbeafe;
  --blue-hover: #1d4ed8;
  --blue-text-on-light: #1e40af;

  /* Red Palette */
  --deep-red: #991b1b;
  --medium-red: #dc2626;
  --light-red: #fee2e2;
  --red-hover: #b91c1c;
  --red-text-on-light: #b91c1c;

  /* Neutrals */
  --background: #ffffff;
  --surface: #f9fafb;
  --border: #e5e7eb;
  --grey-dark: #374151;
  --grey-medium: #9ca3af;
  --grey-light: #f3f4f6;

  /* Button Specific Colors */
  --btn-blue-bg: #2563eb;
  --btn-blue-text: #ffffff;
  --btn-blue-hover-bg: #1d4ed8;
  --btn-blue-outline-border: #2563eb;
  --btn-blue-outline-text: #1e40af;
  --btn-blue-outline-hover-bg: #dbeafe;

  --btn-red-bg: #dc2626;
  --btn-red-text: #ffffff;
  --btn-red-hover-bg: #b91c1c;
  --btn-red-outline-border: #dc2626;
  --btn-red-outline-text: #b91c1c;
  --btn-red-outline-hover-bg: #fee2e2;

  --btn-grey-bg: #6b7280;
  --btn-grey-text: #ffffff;
  --btn-grey-hover-bg: #4b5563;
  --btn-grey-outline-border: #9ca3af;
  --btn-grey-outline-text: #4a4a4a;
  --btn-grey-outline-hover-bg: #f3f4f6;

  /* Legacy names (mapped to new palette) */
  --pale-oak: #f9fafb;
  --ash-grey: #e5e7eb;
  --muted-teal: #dc2626;
  --slate-grey: #991b1b;
  --dusty-grape: #1e3a8a;

  /* CSS HSL */
  --text-primary-hsl: hsla(0, 0%, 10%, 1);
  --text-secondary-hsl: hsla(0, 0%, 29%, 1);
  --text-muted-hsl: hsla(220, 9%, 46%, 1);
  --text-inverse-hsl: hsla(0, 0%, 100%, 1);
  --deep-blue-hsl: hsla(221, 68%, 33%, 1);
  --medium-blue-hsl: hsla(221, 83%, 53%, 1);
  --light-blue-hsl: hsla(214, 95%, 93%, 1);
  --deep-red-hsl: hsla(0, 70%, 35%, 1);
  --medium-red-hsl: hsla(0, 73%, 50%, 1);
  --light-red-hsl: hsla(0, 93%, 94%, 1);
  --background-hsl: hsla(0, 0%, 100%, 1);
  --surface-hsl: hsla(220, 14%, 98%, 1);
  --border-hsl: hsla(220, 13%, 91%, 1);
}
```

### SCSS Variables

```scss
/* Text Colors */
$text-primary: #1a1a1a;
$text-secondary: #4a4a4a;
$text-muted: #6b7280;
$text-inverse: #ffffff;

/* Blue Palette */
$deep-blue: #1e3a8a;
$medium-blue: #2563eb;
$light-blue: #dbeafe;
$blue-hover: #1d4ed8;
$blue-text-on-light: #1e40af;

/* Red Palette */
$deep-red: #991b1b;
$medium-red: #dc2626;
$light-red: #fee2e2;
$red-hover: #b91c1c;
$red-text-on-light: #b91c1c;

/* Neutrals */
$background: #ffffff;
$surface: #f9fafb;
$border: #e5e7eb;
$grey-dark: #374151;
$grey-medium: #9ca3af;
$grey-light: #f3f4f6;

/* Button Specific Colors */
$btn-blue-bg: #2563eb;
$btn-blue-text: #ffffff;
$btn-blue-hover-bg: #1d4ed8;
$btn-blue-outline-border: #2563eb;
$btn-blue-outline-text: #1e40af;
$btn-blue-outline-hover-bg: #dbeafe;

$btn-red-bg: #dc2626;
$btn-red-text: #ffffff;
$btn-red-hover-bg: #b91c1c;
$btn-red-outline-border: #dc2626;
$btn-red-outline-text: #b91c1c;
$btn-red-outline-hover-bg: #fee2e2;

$btn-grey-bg: #6b7280;
$btn-grey-text: #ffffff;
$btn-grey-hover-bg: #4b5563;
$btn-grey-outline-border: #9ca3af;
$btn-grey-outline-text: #4a4a4a;
$btn-grey-outline-hover-bg: #f3f4f6;

/* SCSS HSL */
$text-primary-hsl: hsla(0, 0%, 10%, 1);
$text-inverse-hsl: hsla(0, 0%, 100%, 1);
$deep-blue-hsl: hsla(221, 68%, 33%, 1);
$medium-blue-hsl: hsla(221, 83%, 53%, 1);
$light-blue-hsl: hsla(214, 95%, 93%, 1);
$deep-red-hsl: hsla(0, 70%, 35%, 1);
$medium-red-hsl: hsla(0, 73%, 50%, 1);
$light-red-hsl: hsla(0, 93%, 94%, 1);

/* SCSS RGB */
$text-primary-rgb: rgba(26, 26, 26, 1);
$text-secondary-rgb: rgba(74, 74, 74, 1);
$text-muted-rgb: rgba(107, 114, 128, 1);
$text-inverse-rgb: rgba(255, 255, 255, 1);
$deep-blue-rgb: rgba(30, 58, 138, 1);
$medium-blue-rgb: rgba(37, 99, 235, 1);
$light-blue-rgb: rgba(219, 234, 254, 1);
$deep-red-rgb: rgba(153, 27, 27, 1);
$medium-red-rgb: rgba(220, 38, 38, 1);
$light-red-rgb: rgba(254, 226, 226, 1);
$background-rgb: rgba(255, 255, 255, 1);
$surface-rgb: rgba(249, 250, 251, 1);
$border-rgb: rgba(229, 231, 235, 1);

/* Gradients */
$gradient-top: linear-gradient(
  0deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-right: linear-gradient(
  90deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-bottom: linear-gradient(
  180deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-left: linear-gradient(
  270deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-top-right: linear-gradient(
  45deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-bottom-right: linear-gradient(
  135deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-top-left: linear-gradient(
  225deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-bottom-left: linear-gradient(
  315deg,
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
$gradient-radial: radial-gradient(
  $light-blue,
  $medium-blue,
  $deep-blue,
  $medium-red,
  $deep-red
);
```

## Button Usage Guidelines

### Solid Buttons (High Emphasis)

```css
/* Primary Blue Button */
.btn-primary {
  background: var(--btn-blue-bg);
  color: var(--btn-blue-text);
  border: none;
}
.btn-primary:hover {
  background: var(--btn-blue-hover-bg);
}

/* Danger/Alert Red Button */
.btn-danger {
  background: var(--btn-red-bg);
  color: var(--btn-red-text);
  border: none;
}
.btn-danger:hover {
  background: var(--btn-red-hover-bg);
}

/* Secondary Grey Button */
.btn-secondary {
  background: var(--btn-grey-bg);
  color: var(--btn-grey-text);
  border: none;
}
.btn-secondary:hover {
  background: var(--btn-grey-hover-bg);
}
```

### Outline Buttons (Medium Emphasis)

```css
/* Outline Blue Button */
.btn-outline-primary {
  background: transparent;
  color: var(--btn-blue-outline-text);
  border: 2px solid var(--btn-blue-outline-border);
}
.btn-outline-primary:hover {
  background: var(--btn-blue-outline-hover-bg);
  color: var(--btn-blue-outline-text);
}

/* Outline Red Button */
.btn-outline-danger {
  background: transparent;
  color: var(--btn-red-outline-text);
  border: 2px solid var(--btn-red-outline-border);
}
.btn-outline-danger:hover {
  background: var(--btn-red-outline-hover-bg);
  color: var(--btn-red-outline-text);
}

/* Outline Grey Button */
.btn-outline-secondary {
  background: transparent;
  color: var(--btn-grey-outline-text);
  border: 2px solid var(--btn-grey-outline-border);
}
.btn-outline-secondary:hover {
  background: var(--btn-grey-outline-hover-bg);
  color: var(--btn-grey-outline-text);
}
```

## Usage Guidelines for Text-Heavy Sites

- **Proportions**: 70% neutrals/text colors, 20% blue (primary), 10% red (accents/alerts)
- **Blue Usage**: Headings, links, navigation, primary actions
- **Red Usage**: Warnings, errors, high-priority CTAs, important callouts
- **Grey Usage**: Secondary actions, cancel buttons, disabled states
- **Contrast**: All button combinations exceed 4.5:1 ratio (WCAG AA compliance)
- **Light Tints**: Use `--light-blue` and `--light-red` only for subtle backgrounds and highlights

## Aesthetic Guidelines

- **Visual Style**: Premium, modern, and dynamic with high readability focus
- **Typography**: Modern fonts (e.g., Inter, Roboto, Outfit) with clear hierarchy
- **Interactions**: Hover effects, subtle micro-animations, smooth transitions
- **Design System**: Strict adherence to color palette and Material UI components
- **Accessibility**: All text and interactive elements meet WCAG AA standards (minimum 4.5:1 contrast ratio)
- **Button Hierarchy**: Use solid buttons for primary actions, outline buttons for secondary actions, and text/link buttons for tertiary actions

## Functional Guidelines

- Ensure each page has it's folder and house the components it owns.
- Shared utilities should be in `src/utils`.
- Avoid using useEffect when possible.
- Use useMemo and useCallback where possible.
