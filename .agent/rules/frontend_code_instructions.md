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
  /* CSS HEX */
  --pale-oak: #eeeeeeff;
  --ash-grey: #dededeff;
  --muted-teal: #ff4949ff;
  --slate-grey: #c10000ff;
  --dusty-grape: #8b0000ff;

  /* CSS HSL */
  --pale-oak-hsl: hsla(0, 0%, 93%, 1);
  --ash-grey-hsl: hsla(0, 0%, 87%, 1);
  --muted-teal-hsl: hsla(0, 100%, 64%, 1);
  --slate-grey-hsl: hsla(0, 100%, 38%, 1);
  --dusty-grape-hsl: hsla(0, 100%, 27%, 1);
}
```

### SCSS Variables

```scss
/* SCSS HEX */
$pale-oak: #eeeeeeff;
$ash-grey: #dededeff;
$muted-teal: #ff4949ff;
$slate-grey: #c10000ff;
$dusty-grape: #8b0000ff;

/* SCSS HSL */
$pale-oak-hsl: hsla(0, 0%, 93%, 1);
$ash-grey-hsl: hsla(0, 0%, 87%, 1);
$muted-teal-hsl: hsla(0, 100%, 64%, 1);
$slate-grey-hsl: hsla(0, 100%, 38%, 1);
$dusty-grape-hsl: hsla(0, 100%, 27%, 1);

/* SCSS RGB */
$pale-oak-rgb: rgba(238, 238, 238, 1);
$ash-grey-rgb: rgba(222, 222, 222, 1);
$muted-teal-rgb: rgba(255, 73, 73, 1);
$slate-grey-rgb: rgba(193, 0, 0, 1);
$dusty-grape-rgb: rgba(139, 0, 0, 1);

/* Gradients */
$gradient-top: linear-gradient(
  0deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-right: linear-gradient(
  90deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-bottom: linear-gradient(
  180deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-left: linear-gradient(
  270deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-top-right: linear-gradient(
  45deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-bottom-right: linear-gradient(
  135deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-top-left: linear-gradient(
  225deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-bottom-left: linear-gradient(
  315deg,
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
$gradient-radial: radial-gradient(
  #eeeeeeff,
  #dededeff,
  #ff4949ff,
  #c10000ff,
  #8b0000ff
);
```

## Aesthetic Guidelines

- **Visual Style**: Premium, modern, and dynamic.
- **Typography**: Modern fonts (e.g., Inter, Roboto, Outfit).
- **Interactions**: Use hover effects, subtle micro-animations, and smooth transitions.
- **Design System**: Strict adherence to the color palette and Material UI components.

## Functional Guidelines

- Ensure each page has it's folder and house the components it owns.
- Shared utilities should be in `src/utils`.
- Avoid using useEffect when possible.
- Use useMemo and useCallback where possible.
