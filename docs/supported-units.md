# Supported Units

This page lists exact unit labels accepted by `convert()`. The filter
uses source categories from the bundled standard. Applications that
need display categories can use `get_ui_unit_catalog()` together with
`get_unit_catalog()["units"]`.

## Browse By Category

<div class="unit-filter-panel">
  <label for="unit-category-filter">Category</label>
  <select id="unit-category-filter" class="unit-filter-select">
    <option value="__all__">All categories</option>
    <option value="acceleration">ACCELERATION (5 units)</option>
    <option value="angle">ANGLE (7 units)</option>
    <option value="area-and-second-moment-of-area">AREA AND SECOND MOMENT OF AREA (17 units)</option>
    <option value="electricity-and-magnetism">ELECTRICITY and MAGNETISM (50 units)</option>
    <option value="energy">ENERGY (includes WORK) (30 units)</option>
    <option value="energy-divided-by-area-time">ENERGY DIVIDED BY AREA TIME (4 units)</option>
    <option value="force">FORCE (12 units)</option>
    <option value="force-divided-by-length">FORCE DIVIDED BY LENGTH (3 units)</option>
    <option value="heat">HEAT (84 units)</option>
    <option value="length">LENGTH (32 units)</option>
    <option value="light">LIGHT (9 units)</option>
    <option value="mass-and-moment-of-inertia">MASS and MOMENT OF INERTIA (23 units)</option>
    <option value="mass-divided-by-area">MASS DIVIDED BY AREA (6 units)</option>
    <option value="mass-divided-by-length">MASS DIVIDED BY LENGTH (7 units)</option>
    <option value="mass-divided-by-time">MASS DIVIDED BY TIME (includes FLOW) (5 units)</option>
    <option value="mass-divided-by-volume">MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS CONCENTRATION) (17 units)</option>
    <option value="moment-of-force-or-torque">MOMENT OF FORCE or TORQUE (8 units)</option>
    <option value="moment-of-force-or-torque-divided-by-length">MOMENT OF FORCE or TORQUE, DIVIDED BY LENGTH (3 units)</option>
    <option value="permeability">PERMEABILITY (8 units)</option>
    <option value="power">POWER (11 units)</option>
    <option value="pressure-or-stress">PRESSURE or STRESS (FORCE DIVIDED BY AREA) (33 units)</option>
    <option value="radiology">RADIOLOGY (8 units)</option>
    <option value="temperature">TEMPERATURE (5 units)</option>
    <option value="temperature-interval">TEMPERATURE INTERVAL (5 units)</option>
    <option value="time">TIME (13 units)</option>
    <option value="velocity">VELOCITY (includes SPEED) (13 units)</option>
    <option value="viscosity-dynamic">VISCOSITY, DYNAMIC (11 units)</option>
    <option value="viscosity-kinematic">VISCOSITY, KINEMATIC (4 units)</option>
    <option value="volume">VOLUME (includes CAPACITY) (28 units)</option>
    <option value="volume-divided-by-time">VOLUME DIVIDED BY TIME (includes FLOW) (8 units)</option>
  </select>
  <p id="unit-filter-count" class="unit-filter-count"></p>
</div>

<div id="unit-category-list">
<section class="unit-category" data-category="acceleration" data-category-name="ACCELERATION" data-unit-count="5">
<h2 id="acceleration">ACCELERATION</h2>
<p class="unit-category-count">5 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>acceleration of free fall, standard (gn)</code></td></tr>
    <tr><td><code>foot per second squared (ft / s2)</code></td></tr>
    <tr><td><code>gal (Gal)</code></td></tr>
    <tr><td><code>inch per second squared (in / s2)</code></td></tr>
    <tr><td><code>meter per second squared (m / s2)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="angle" data-category-name="ANGLE" data-unit-count="7">
<h2 id="angle">ANGLE</h2>
<p class="unit-category-count">7 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>degree (°)</code></td></tr>
    <tr><td><code>gon (also called grade) (gon)</code></td></tr>
    <tr><td><code>mil</code></td></tr>
    <tr><td><code>minute (&#x27;)</code></td></tr>
    <tr><td><code>radian (rad)</code></td></tr>
    <tr><td><code>revolution (r)</code></td></tr>
    <tr><td><code>second (&quot;)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="area-and-second-moment-of-area" data-category-name="AREA AND SECOND MOMENT OF AREA" data-unit-count="17">
<h2 id="area-and-second-moment-of-area">AREA AND SECOND MOMENT OF AREA</h2>
<p class="unit-category-count">17 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>acre (based on U.S. survey foot)</code></td></tr>
    <tr><td><code>are (a)</code></td></tr>
    <tr><td><code>barn (b)</code></td></tr>
    <tr><td><code>circular mil</code></td></tr>
    <tr><td><code>foot to the fourth power (ft4)</code></td></tr>
    <tr><td><code>hectare (ha)</code></td></tr>
    <tr><td><code>inch to the fourth power (in4)</code></td></tr>
    <tr><td><code>meter to the fourth power (m4)</code></td></tr>
    <tr><td><code>square centimeter (cm2)</code></td></tr>
    <tr><td><code>square foot (ft2)</code></td></tr>
    <tr><td><code>square inch (in2)</code></td></tr>
    <tr><td><code>square kilometer (km2)</code></td></tr>
    <tr><td><code>square meter (m2)</code></td></tr>
    <tr><td><code>square mile (based on U.S. survey foot) (mi2)</code></td></tr>
    <tr><td><code>square mile (mi2)</code></td></tr>
    <tr><td><code>square millimeter (mm2)</code></td></tr>
    <tr><td><code>square yard (yd2)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="electricity-and-magnetism" data-category-name="ELECTRICITY and MAGNETISM" data-unit-count="50">
<h2 id="electricity-and-magnetism">ELECTRICITY and MAGNETISM</h2>
<p class="unit-category-count">50 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>EMU of capacitance (abfarad)</code></td></tr>
    <tr><td><code>EMU of current (abampere)</code></td></tr>
    <tr><td><code>EMU of electric potential (abvolt)</code></td></tr>
    <tr><td><code>EMU of inductance (abhenry)</code></td></tr>
    <tr><td><code>EMU of resistance (abohm)</code></td></tr>
    <tr><td><code>ESU of capacitance (statfarad)</code></td></tr>
    <tr><td><code>ESU of current (statampere)</code></td></tr>
    <tr><td><code>ESU of electric potential (statvolt)</code></td></tr>
    <tr><td><code>ESU of inductance (stathenry)</code></td></tr>
    <tr><td><code>ESU of resistance (statohm)</code></td></tr>
    <tr><td><code>abampere</code></td></tr>
    <tr><td><code>abcoulomb</code></td></tr>
    <tr><td><code>abfarad</code></td></tr>
    <tr><td><code>abhenry</code></td></tr>
    <tr><td><code>abmho</code></td></tr>
    <tr><td><code>abohm</code></td></tr>
    <tr><td><code>abvolt</code></td></tr>
    <tr><td><code>ampere (A)</code></td></tr>
    <tr><td><code>ampere hour (A · h)</code></td></tr>
    <tr><td><code>ampere per meter (A / m)</code></td></tr>
    <tr><td><code>biot (Bi)</code></td></tr>
    <tr><td><code>coulomb (C)</code></td></tr>
    <tr><td><code>farad (F)</code></td></tr>
    <tr><td><code>faraday (based on carbon 12)</code></td></tr>
    <tr><td><code>franklin (Fr)</code></td></tr>
    <tr><td><code>gamma (γ)</code></td></tr>
    <tr><td><code>gauss (Gs, G)</code></td></tr>
    <tr><td><code>gilbert (Gi)</code></td></tr>
    <tr><td><code>henry (H)</code></td></tr>
    <tr><td><code>maxwell (Mx)</code></td></tr>
    <tr><td><code>mho</code></td></tr>
    <tr><td><code>oersted (Oe)</code></td></tr>
    <tr><td><code>ohm ( Ω)</code></td></tr>
    <tr><td><code>ohm (Ω)</code></td></tr>
    <tr><td><code>ohm centimeter (Ω · cm)</code></td></tr>
    <tr><td><code>ohm circular-mil per foot</code></td></tr>
    <tr><td><code>ohm meter ( Ω · m)</code></td></tr>
    <tr><td><code>ohm square millimeter per meter (Ω · mm2 / m)</code></td></tr>
    <tr><td><code>siemens (S)</code></td></tr>
    <tr><td><code>statampere</code></td></tr>
    <tr><td><code>statcoulomb</code></td></tr>
    <tr><td><code>statfarad</code></td></tr>
    <tr><td><code>stathenry</code></td></tr>
    <tr><td><code>statmho</code></td></tr>
    <tr><td><code>statohm</code></td></tr>
    <tr><td><code>statvolt</code></td></tr>
    <tr><td><code>tesla (T)</code></td></tr>
    <tr><td><code>unit pole</code></td></tr>
    <tr><td><code>volt (V)</code></td></tr>
    <tr><td><code>weber (Wb)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="energy" data-category-name="ENERGY (includes WORK)" data-unit-count="30">
<h2 id="energy">ENERGY (includes WORK)</h2>
<p class="unit-category-count">30 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>British thermal unit (39 °F) (Btu)</code></td></tr>
    <tr><td><code>British thermal unit (59 °F) (Btu)</code></td></tr>
    <tr><td><code>British thermal unit (60 °F) (Btu)</code></td></tr>
    <tr><td><code>British thermal unit (mean) (Btu)</code></td></tr>
    <tr><td><code>British thermal unitIT (BtuIT)</code></td></tr>
    <tr><td><code>British thermal unitth (Btuth)</code></td></tr>
    <tr><td><code>calorie (15 °C) (cal15)</code></td></tr>
    <tr><td><code>calorie (20 °C) (cal20)</code></td></tr>
    <tr><td><code>calorie (mean) (cal)</code></td></tr>
    <tr><td><code>calorie (mean), kilogram (nutrition)</code></td></tr>
    <tr><td><code>calorieIT (calIT)</code></td></tr>
    <tr><td><code>calorieIT, kilogram (nutrition)</code></td></tr>
    <tr><td><code>calorieth (calth)</code></td></tr>
    <tr><td><code>calorieth, kilogram (nutrition)</code></td></tr>
    <tr><td><code>electronvolt (eV)</code></td></tr>
    <tr><td><code>erg (erg)</code></td></tr>
    <tr><td><code>foot pound-force (ft · lbf)</code></td></tr>
    <tr><td><code>foot poundal</code></td></tr>
    <tr><td><code>joule (J)</code></td></tr>
    <tr><td><code>kilocalorie (mean) (kcal)</code></td></tr>
    <tr><td><code>kilocalorieIT (kcalIT)</code></td></tr>
    <tr><td><code>kilocalorieth (kcalth)</code></td></tr>
    <tr><td><code>kilowatt hour (kW · h)</code></td></tr>
    <tr><td><code>megajoule (MJ)</code></td></tr>
    <tr><td><code>quad (1015 BtuIT)</code></td></tr>
    <tr><td><code>therm (EC)</code></td></tr>
    <tr><td><code>therm (U.S.)</code></td></tr>
    <tr><td><code>ton of TNT (energy equivalent)</code></td></tr>
    <tr><td><code>watt hour (W · h)</code></td></tr>
    <tr><td><code>watt second (W · s)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="energy-divided-by-area-time" data-category-name="ENERGY DIVIDED BY AREA TIME" data-unit-count="4">
<h2 id="energy-divided-by-area-time">ENERGY DIVIDED BY AREA TIME</h2>
<p class="unit-category-count">4 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>erg per square centimeter second [erg / (cm2 · s)]</code></td></tr>
    <tr><td><code>watt per square centimeter (W / cm2)</code></td></tr>
    <tr><td><code>watt per square inch (W / in2)</code></td></tr>
    <tr><td><code>watt per square meter (W / m2)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="force" data-category-name="FORCE" data-unit-count="12">
<h2 id="force">FORCE</h2>
<p class="unit-category-count">12 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>dyne (dyn)</code></td></tr>
    <tr><td><code>kilogram-force (kgf)</code></td></tr>
    <tr><td><code>kilonewton (kN)</code></td></tr>
    <tr><td><code>kilopond (kilogram-force) (kp)</code></td></tr>
    <tr><td><code>kip (1 kip = 1000 lbf)</code></td></tr>
    <tr><td><code>newton (N)</code></td></tr>
    <tr><td><code>newton per kilogram (N / kg)</code></td></tr>
    <tr><td><code>ounce (avoirdupois)-force (ozf)</code></td></tr>
    <tr><td><code>pound-force (lbf)</code></td></tr>
    <tr><td><code>pound-force per pound (lbf / lb) (thrust to mass ratio)</code></td></tr>
    <tr><td><code>poundal</code></td></tr>
    <tr><td><code>ton-force (2000 lbf)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="force-divided-by-length" data-category-name="FORCE DIVIDED BY LENGTH" data-unit-count="3">
<h2 id="force-divided-by-length">FORCE DIVIDED BY LENGTH</h2>
<p class="unit-category-count">3 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>newton per meter (N / m)</code></td></tr>
    <tr><td><code>pound-force per foot (lbf / ft)</code></td></tr>
    <tr><td><code>pound-force per inch (lbf / in)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="heat" data-category-name="HEAT" data-unit-count="84">
<h2 id="heat">HEAT</h2>
<p class="unit-category-count">84 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>British thermal unitIT foot per hour square foot degree Fahrenheit [Btu IT · ft / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT inch per hour square foot degree Fahrenheit [Btu IT · in / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT inch per second square foot degree Fahrenheit [Btu IT · in / (s · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT per cubic foot (BtuIT / ft3)</code></td></tr>
    <tr><td><code>British thermal unitIT per degree Fahrenheit (Btu IT / °F)</code></td></tr>
    <tr><td><code>British thermal unitIT per degree Rankine (Btu IT / °R)</code></td></tr>
    <tr><td><code>British thermal unitIT per hour (BtuIT / h)</code></td></tr>
    <tr><td><code>British thermal unitIT per hour square foot degree Fahrenheit [Btu IT / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT per pound (BtuIT / lb)</code></td></tr>
    <tr><td><code>British thermal unitIT per pound degree Fahrenheit [Btu IT / (lb · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT per pound degree Rankine [Btu IT / (lb · °R)]</code></td></tr>
    <tr><td><code>British thermal unitIT per second (BtuIT / s)</code></td></tr>
    <tr><td><code>British thermal unitIT per second square foot degree Fahrenheit [Btu IT / (s · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitIT per square foot (Btu IT / ft2)</code></td></tr>
    <tr><td><code>British thermal unitIT per square foot hour [Btu IT / (ft2 · h)]</code></td></tr>
    <tr><td><code>British thermal unitIT per square foot second [Btu IT / (ft2 · s)]</code></td></tr>
    <tr><td><code>British thermal unitth foot per hour square foot degree Fahrenheit [Btu th · ft / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth inch per hour square foot degree Fahrenheit [Btu th · in / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth inch per second square foot degree Fahrenheit [Btu th · in / (s · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth per cubic foot (Btuth / ft3)</code></td></tr>
    <tr><td><code>British thermal unitth per degree Fahrenheit (Btu th / °F)</code></td></tr>
    <tr><td><code>British thermal unitth per degree Rankine (Btu th / °R)</code></td></tr>
    <tr><td><code>British thermal unitth per hour (Btuth / h)</code></td></tr>
    <tr><td><code>British thermal unitth per hour square foot degree Fahrenheit [Btu th / (h · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth per minute (Btuth / min)</code></td></tr>
    <tr><td><code>British thermal unitth per pound (Btuth / lb)</code></td></tr>
    <tr><td><code>British thermal unitth per pound degree Fahrenheit [Btu th / (lb · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth per pound degree Rankine [Btu th / (lb · °R)]</code></td></tr>
    <tr><td><code>British thermal unitth per second (Btuth / s)</code></td></tr>
    <tr><td><code>British thermal unitth per second square foot degree Fahrenheit [Btu th / (s · ft2 · °F)]</code></td></tr>
    <tr><td><code>British thermal unitth per square foot (Btu th / ft2)</code></td></tr>
    <tr><td><code>British thermal unitth per square foot hour [Btu th / (ft2 · h)]</code></td></tr>
    <tr><td><code>British thermal unitth per square foot minute [Btu th / (ft2 · min)]</code></td></tr>
    <tr><td><code>British thermal unitth per square foot second [Btu th / (ft2 · s)]</code></td></tr>
    <tr><td><code>British thermal unitth per square inch second [Btu th / (in2 · s)]</code></td></tr>
    <tr><td><code>calorieIT per gram (calIT / g)</code></td></tr>
    <tr><td><code>calorieIT per gram degree Celsius [cal IT / (g · °C)]</code></td></tr>
    <tr><td><code>calorieIT per gram kelvin [calIT / (g · K)]</code></td></tr>
    <tr><td><code>calorieth per centimeter second degree Celsius [cal th / (cm · s · °C)]</code></td></tr>
    <tr><td><code>calorieth per gram (calth / g)</code></td></tr>
    <tr><td><code>calorieth per gram degree Celsius [cal th / (g · °C)]</code></td></tr>
    <tr><td><code>calorieth per gram kelvin [calth / (g · K)]</code></td></tr>
    <tr><td><code>calorieth per minute (calth / min)</code></td></tr>
    <tr><td><code>calorieth per second (calth / s)</code></td></tr>
    <tr><td><code>calorieth per square centimeter (calth / cm2)</code></td></tr>
    <tr><td><code>calorieth per square centimeter minute [cal th / (cm2 · min)]</code></td></tr>
    <tr><td><code>calorieth per square centimeter second [cal th / (cm2 · s)]</code></td></tr>
    <tr><td><code>clo</code></td></tr>
    <tr><td><code>cubic meter per joule (m3 / J)</code></td></tr>
    <tr><td><code>degree Fahrenheit hour per British thermal unitIT (°F · h / Btu IT)</code></td></tr>
    <tr><td><code>degree Fahrenheit hour per British thermal unitth (°F · h / Btu th)</code></td></tr>
    <tr><td><code>degree Fahrenheit hour square foot per British thermal unit th (°F · h · ft2 / Btuth)</code></td></tr>
    <tr><td><code>degree Fahrenheit hour square foot per British thermal unitIT (°F · h · ft2 / BtuIT)</code></td></tr>
    <tr><td><code>degree Fahrenheit hour square foot per British thermal unitIT inch [°F · h · ft2 / (BtuIT · in)]</code></td></tr>
    <tr><td><code>degree Fahrenheit hour square foot per British thermal unitth inch [°F · h · ft2 / (Btuth · in)]</code></td></tr>
    <tr><td><code>degree Fahrenheit second per British thermal unitIT (°F · s / Btu IT)</code></td></tr>
    <tr><td><code>degree Fahrenheit second per British thermal unitth (°F · s / Btu th)</code></td></tr>
    <tr><td><code>gallon (U.S.) per horsepower hour [gal / (hp · h)]</code></td></tr>
    <tr><td><code>joule per cubic meter (J / m3)</code></td></tr>
    <tr><td><code>joule per kelvin (J / K)</code></td></tr>
    <tr><td><code>joule per kilogram (J / kg)</code></td></tr>
    <tr><td><code>joule per kilogram kelvin [J / (kg · K)]</code></td></tr>
    <tr><td><code>joule per square meter (J / m2)</code></td></tr>
    <tr><td><code>kelvin per watt (K / W)</code></td></tr>
    <tr><td><code>kilocalorieth per minute (kcalth / min)</code></td></tr>
    <tr><td><code>kilocalorieth per second (kcalth / s)</code></td></tr>
    <tr><td><code>kilogram per joule (kg / J)</code></td></tr>
    <tr><td><code>kilometer per liter (km / L)</code></td></tr>
    <tr><td><code>langley (calth / cm2)</code></td></tr>
    <tr><td><code>liter per 100 kilometer (L / 100 km)</code></td></tr>
    <tr><td><code>liter per joule (L / J)</code></td></tr>
    <tr><td><code>meter kelvin per watt (m · K / W)</code></td></tr>
    <tr><td><code>meter per cubic meter (m / m3)</code></td></tr>
    <tr><td><code>mile per gallon (U.S.) (mpg) (mi / gal)</code></td></tr>
    <tr><td><code>per gallon pound per horsepower hour [lb / (hp · h)]</code></td></tr>
    <tr><td><code>square foot per hour (ft2 / h)</code></td></tr>
    <tr><td><code>square meter kelvin per watt (m2 · K / W)</code></td></tr>
    <tr><td><code>square meter per second (m2 / s)</code></td></tr>
    <tr><td><code>ton of refrigeration (12 000 BtuIT / h)</code></td></tr>
    <tr><td><code>watt (W)</code></td></tr>
    <tr><td><code>watt per meter kelvin [W / (m · K)]</code></td></tr>
    <tr><td><code>watt per square meter (W / m2)</code></td></tr>
    <tr><td><code>watt per square meter Kelvin [W / (m2 · K)]</code></td></tr>
    <tr><td><code>watt per square meter kelvin [W / (m2 · K)]</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="length" data-category-name="LENGTH" data-unit-count="32">
<h2 id="length">LENGTH</h2>
<p class="unit-category-count">32 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>astronomical unit (ua)</code></td></tr>
    <tr><td><code>centimeter (cm)</code></td></tr>
    <tr><td><code>chain (based on U.S. survey foot) (ch)</code></td></tr>
    <tr><td><code>fathom (based on U.S. survey foot)</code></td></tr>
    <tr><td><code>femtometer (fm)</code></td></tr>
    <tr><td><code>fermi</code></td></tr>
    <tr><td><code>foot (U.S. survey) (ft)</code></td></tr>
    <tr><td><code>foot (ft)</code></td></tr>
    <tr><td><code>inch (in)</code></td></tr>
    <tr><td><code>kayser (K)</code></td></tr>
    <tr><td><code>kilometer (km)</code></td></tr>
    <tr><td><code>light year (l.y.)</code></td></tr>
    <tr><td><code>meter (m)</code></td></tr>
    <tr><td><code>microinch</code></td></tr>
    <tr><td><code>micrometer ( μm)</code></td></tr>
    <tr><td><code>micron (μ)</code></td></tr>
    <tr><td><code>mil (0.001 in)</code></td></tr>
    <tr><td><code>mil limeter (mm)</code></td></tr>
    <tr><td><code>mile (based on U.S. survey foot) (mi)</code></td></tr>
    <tr><td><code>mile (mi)</code></td></tr>
    <tr><td><code>mile, nautical</code></td></tr>
    <tr><td><code>millimeter (mm)</code></td></tr>
    <tr><td><code>nanometer (nm)</code></td></tr>
    <tr><td><code>parsec (pc)</code></td></tr>
    <tr><td><code>pica (computer) (1/6 in)</code></td></tr>
    <tr><td><code>pica (printer’s)</code></td></tr>
    <tr><td><code>point (computer) (1/72 in)</code></td></tr>
    <tr><td><code>point (printer’s)</code></td></tr>
    <tr><td><code>reciprocal meter (m ^-1)</code></td></tr>
    <tr><td><code>rod (based on U.S. survey foot) (rd)</code></td></tr>
    <tr><td><code>yard (yd)</code></td></tr>
    <tr><td><code>ångström (Å)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="light" data-category-name="LIGHT" data-unit-count="9">
<h2 id="light">LIGHT</h2>
<p class="unit-category-count">9 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>candela per square inch (cd / in2)</code></td></tr>
    <tr><td><code>candela per square meter (cd / m2)</code></td></tr>
    <tr><td><code>footcandle</code></td></tr>
    <tr><td><code>footlambert</code></td></tr>
    <tr><td><code>lambert</code></td></tr>
    <tr><td><code>lumen per square foot (lm / ft2)</code></td></tr>
    <tr><td><code>lux (lx)</code></td></tr>
    <tr><td><code>phot (ph)</code></td></tr>
    <tr><td><code>stilb (sb)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="mass-and-moment-of-inertia" data-category-name="MASS and MOMENT OF INERTIA" data-unit-count="23">
<h2 id="mass-and-moment-of-inertia">MASS and MOMENT OF INERTIA</h2>
<p class="unit-category-count">23 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>carat, metric</code></td></tr>
    <tr><td><code>grain (gr)</code></td></tr>
    <tr><td><code>gram (g)</code></td></tr>
    <tr><td><code>hundredweight (long, 112 lb)</code></td></tr>
    <tr><td><code>hundredweight (short, 100 lb)</code></td></tr>
    <tr><td><code>kilogram (k g)</code></td></tr>
    <tr><td><code>kilogram (kg)</code></td></tr>
    <tr><td><code>kilogram meter squared (kg · m2)</code></td></tr>
    <tr><td><code>kilogram-force second squared per meter (kgf · s2 / m)</code></td></tr>
    <tr><td><code>milligram (mg)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) (oz)</code></td></tr>
    <tr><td><code>ounce (troy or apothecary) (oz)</code></td></tr>
    <tr><td><code>pennyweight (dwt)</code></td></tr>
    <tr><td><code>pound (avoirdupois) (lb)</code></td></tr>
    <tr><td><code>pound (troy or apothecary) (lb)</code></td></tr>
    <tr><td><code>pound foot squared (lb · ft2)</code></td></tr>
    <tr><td><code>pound inch squared (lb · in2)</code></td></tr>
    <tr><td><code>slug (slug)</code></td></tr>
    <tr><td><code>ton, assay (AT)</code></td></tr>
    <tr><td><code>ton, long (2240 lb)</code></td></tr>
    <tr><td><code>ton, metric (t)</code></td></tr>
    <tr><td><code>ton, short (2000 lb)</code></td></tr>
    <tr><td><code>tonne (called “metric ton” in U.S.) (t)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="mass-divided-by-area" data-category-name="MASS DIVIDED BY AREA" data-unit-count="6">
<h2 id="mass-divided-by-area">MASS DIVIDED BY AREA</h2>
<p class="unit-category-count">6 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>kilogram per square meter (kg / m2)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per square foot (oz / ft2)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per square inch (oz / in2)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per square yard (oz / yd2)</code></td></tr>
    <tr><td><code>pound per square foot (lb / ft2)</code></td></tr>
    <tr><td><code>pound per square inch (not pound force) (lb / in2)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="mass-divided-by-length" data-category-name="MASS DIVIDED BY LENGTH" data-unit-count="7">
<h2 id="mass-divided-by-length">MASS DIVIDED BY LENGTH</h2>
<p class="unit-category-count">7 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>denier</code></td></tr>
    <tr><td><code>gram per meter (g / m)</code></td></tr>
    <tr><td><code>kilogram per meter (kg / m)</code></td></tr>
    <tr><td><code>pound per foot (lb / ft)</code></td></tr>
    <tr><td><code>pound per inch (lb / in)</code></td></tr>
    <tr><td><code>pound per yard (lb / yd)</code></td></tr>
    <tr><td><code>tex</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="mass-divided-by-time" data-category-name="MASS DIVIDED BY TIME (includes FLOW)" data-unit-count="5">
<h2 id="mass-divided-by-time">MASS DIVIDED BY TIME (includes FLOW)</h2>
<p class="unit-category-count">5 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>kilogram per second (kg / s)</code></td></tr>
    <tr><td><code>pound per hour (lb / h)</code></td></tr>
    <tr><td><code>pound per minute (lb / min)</code></td></tr>
    <tr><td><code>pound per second (lb / s)</code></td></tr>
    <tr><td><code>ton, short, per hour</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="mass-divided-by-volume" data-category-name="MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS CONCENTRATION)" data-unit-count="17">
<h2 id="mass-divided-by-volume">MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS CONCENTRATION)</h2>
<p class="unit-category-count">17 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>grain per gallon (U.S.) (gr / gal)</code></td></tr>
    <tr><td><code>gram per cubic centimeter (g / cm3)</code></td></tr>
    <tr><td><code>gram per liter (g / L)</code></td></tr>
    <tr><td><code>kilogram per cubic meter (kg / m3)</code></td></tr>
    <tr><td><code>kilogram per liter (kg / L)</code></td></tr>
    <tr><td><code>milligram per liter (mg / L)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per cubic inch (oz / in3)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per gallon (U.S.) (oz / gal)</code></td></tr>
    <tr><td><code>ounce (avoirdupois) per gallon [Canadian and U.K. (Imperial)] (oz / gal)</code></td></tr>
    <tr><td><code>pound per cubic foot (lb / ft3)</code></td></tr>
    <tr><td><code>pound per cubic inch (lb / in3)</code></td></tr>
    <tr><td><code>pound per cubic yard (lb / yd3)</code></td></tr>
    <tr><td><code>pound per gallon (U.S.) (lb / gal)</code></td></tr>
    <tr><td><code>pound per gallon [Canadian and U.K. (Imperial)] (lb / gal)</code></td></tr>
    <tr><td><code>slug per cubic foot (slug / ft3)</code></td></tr>
    <tr><td><code>ton, long, per cubic yard</code></td></tr>
    <tr><td><code>ton, short, per cubic yard</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="moment-of-force-or-torque" data-category-name="MOMENT OF FORCE or TORQUE" data-unit-count="8">
<h2 id="moment-of-force-or-torque">MOMENT OF FORCE or TORQUE</h2>
<p class="unit-category-count">8 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>dyne centimeter (dyn · cm)</code></td></tr>
    <tr><td><code>kilogram-force meter (kgf · m)</code></td></tr>
    <tr><td><code>millinewton meter (mN · m)</code></td></tr>
    <tr><td><code>newton meter (N · m)</code></td></tr>
    <tr><td><code>newton meter (N ·m)</code></td></tr>
    <tr><td><code>ounce (avoirdupois)-force inch (ozf · in)</code></td></tr>
    <tr><td><code>pound-force foot (lbf · ft)</code></td></tr>
    <tr><td><code>pound-force inch (lbf · in)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="moment-of-force-or-torque-divided-by-length" data-category-name="MOMENT OF FORCE or TORQUE, DIVIDED BY LENGTH" data-unit-count="3">
<h2 id="moment-of-force-or-torque-divided-by-length">MOMENT OF FORCE or TORQUE, DIVIDED BY LENGTH</h2>
<p class="unit-category-count">3 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>newton meter per meter (N · m / m)</code></td></tr>
    <tr><td><code>pound-force foot per inch (lbf · ft / in)</code></td></tr>
    <tr><td><code>pound-force inch per inch (lbf · in / in)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="permeability" data-category-name="PERMEABILITY" data-unit-count="8">
<h2 id="permeability">PERMEABILITY</h2>
<p class="unit-category-count">8 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>darcy</code></td></tr>
    <tr><td><code>kilogram per pascal second meter [kg / (Pa · s · m)]</code></td></tr>
    <tr><td><code>kilogram per pascal second square meter [kg / (Pa · s · m2)]</code></td></tr>
    <tr><td><code>meter squared (m2)</code></td></tr>
    <tr><td><code>perm (0 °C)</code></td></tr>
    <tr><td><code>perm (23 °C)</code></td></tr>
    <tr><td><code>perm inch (0 °C)</code></td></tr>
    <tr><td><code>perm inch (23 °C)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="power" data-category-name="POWER" data-unit-count="11">
<h2 id="power">POWER</h2>
<p class="unit-category-count">11 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>erg per second (erg / s)</code></td></tr>
    <tr><td><code>foot pound-force per hour (ft · lbf / h)</code></td></tr>
    <tr><td><code>foot pound-force per minute (ft · lbf / min)</code></td></tr>
    <tr><td><code>foot pound-force per second (ft · lbf / s)</code></td></tr>
    <tr><td><code>horsepower (550 ft · lbf / s)</code></td></tr>
    <tr><td><code>horsepower (U.K.)</code></td></tr>
    <tr><td><code>horsepower (boiler)</code></td></tr>
    <tr><td><code>horsepower (electric)</code></td></tr>
    <tr><td><code>horsepower (metric)</code></td></tr>
    <tr><td><code>horsepower (water)</code></td></tr>
    <tr><td><code>watt (W)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="pressure-or-stress" data-category-name="PRESSURE or STRESS (FORCE DIVIDED BY AREA)" data-unit-count="33">
<h2 id="pressure-or-stress">PRESSURE or STRESS (FORCE DIVIDED BY AREA)</h2>
<p class="unit-category-count">33 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>atmosphere, standard (atm)</code></td></tr>
    <tr><td><code>atmosphere, technical (at)</code></td></tr>
    <tr><td><code>bar (bar)</code></td></tr>
    <tr><td><code>centimeter of mercury (0 °C)</code></td></tr>
    <tr><td><code>centimeter of mercury, conventional (cmHg)</code></td></tr>
    <tr><td><code>centimeter of water (4 °C)</code></td></tr>
    <tr><td><code>centimeter of water, conventional (cmH2O)</code></td></tr>
    <tr><td><code>dyne per square centimeter (dyn / cm2)</code></td></tr>
    <tr><td><code>foot of mercury, conventional (ftHg)</code></td></tr>
    <tr><td><code>foot of water (39.2 °F)</code></td></tr>
    <tr><td><code>foot of water, conventional (ftH2O)</code></td></tr>
    <tr><td><code>gram-force per square centimeter (gf / cm2)</code></td></tr>
    <tr><td><code>inch of mercury (32 °F)</code></td></tr>
    <tr><td><code>inch of mercury (60 °F)</code></td></tr>
    <tr><td><code>inch of mercury, conventional (inHg)</code></td></tr>
    <tr><td><code>inch of water (39.2 °F)</code></td></tr>
    <tr><td><code>inch of water (60 °F)</code></td></tr>
    <tr><td><code>inch of water, conventional (inH2O)</code></td></tr>
    <tr><td><code>kilogram-force per square centimeter (kgf / cm2)</code></td></tr>
    <tr><td><code>kilogram-force per square meter (kgf / m2)</code></td></tr>
    <tr><td><code>kilogram-force per square millimeter (kgf / mm2)</code></td></tr>
    <tr><td><code>kilopascal (kPa)</code></td></tr>
    <tr><td><code>kip per square inch (ksi) (kip / in2)</code></td></tr>
    <tr><td><code>megapascal (MPa)</code></td></tr>
    <tr><td><code>millibar (mbar)</code></td></tr>
    <tr><td><code>millimeter of mercury, conventional (mmHg)</code></td></tr>
    <tr><td><code>millimeter of water, conventional (mmH2O)</code></td></tr>
    <tr><td><code>pascal (Pa)</code></td></tr>
    <tr><td><code>pound-force per square foot (lbf / ft2)</code></td></tr>
    <tr><td><code>pound-force per square inch (psi) (lbf / in2)</code></td></tr>
    <tr><td><code>poundal per square foot</code></td></tr>
    <tr><td><code>psi (pound-force per square inch) (lbf / in2)</code></td></tr>
    <tr><td><code>torr (Torr)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="radiology" data-category-name="RADIOLOGY" data-unit-count="8">
<h2 id="radiology">RADIOLOGY</h2>
<p class="unit-category-count">8 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>becquerel (Bq)</code></td></tr>
    <tr><td><code>coulomb per kilogram (C / kg)</code></td></tr>
    <tr><td><code>curie (Ci)</code></td></tr>
    <tr><td><code>gray (Gy)</code></td></tr>
    <tr><td><code>rad (absorbed dose) (rad)</code></td></tr>
    <tr><td><code>rem (rem)</code></td></tr>
    <tr><td><code>roentgen (R)</code></td></tr>
    <tr><td><code>sievert (Sv)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="temperature" data-category-name="TEMPERATURE" data-unit-count="5">
<h2 id="temperature">TEMPERATURE</h2>
<p class="unit-category-count">5 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>degree Celsius (°C) [temperature]</code></td></tr>
    <tr><td><code>degree Fahrenheit (°F) [temperature]</code></td></tr>
    <tr><td><code>degree Rankine (°R) [temperature]</code></td></tr>
    <tr><td><code>degree centigrade [temperature]</code></td></tr>
    <tr><td><code>kelvin (K) [temperature]</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="temperature-interval" data-category-name="TEMPERATURE INTERVAL" data-unit-count="5">
<h2 id="temperature-interval">TEMPERATURE INTERVAL</h2>
<p class="unit-category-count">5 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>degree Celsius (°C) [temperature interval]</code></td></tr>
    <tr><td><code>degree Fahrenheit (°F) [temperature interval]</code></td></tr>
    <tr><td><code>degree Rankine (°R) [temperature interval]</code></td></tr>
    <tr><td><code>degree centigrade [temperature interval]</code></td></tr>
    <tr><td><code>kelvin (K) [temperature interval]</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="time" data-category-name="TIME" data-unit-count="13">
<h2 id="time">TIME</h2>
<p class="unit-category-count">13 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>day (d)</code></td></tr>
    <tr><td><code>day (sidereal)</code></td></tr>
    <tr><td><code>hour (h)</code></td></tr>
    <tr><td><code>hour (sidereal)</code></td></tr>
    <tr><td><code>minute (min)</code></td></tr>
    <tr><td><code>minute (sidereal)</code></td></tr>
    <tr><td><code>nanosecond (ns)</code></td></tr>
    <tr><td><code>second (s)</code></td></tr>
    <tr><td><code>second (sidereal)</code></td></tr>
    <tr><td><code>shake</code></td></tr>
    <tr><td><code>year (365 days)</code></td></tr>
    <tr><td><code>year (sidereal)</code></td></tr>
    <tr><td><code>year (tropical)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="velocity" data-category-name="VELOCITY (includes SPEED)" data-unit-count="13">
<h2 id="velocity">VELOCITY (includes SPEED)</h2>
<p class="unit-category-count">13 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>foot per hour (ft / h)</code></td></tr>
    <tr><td><code>foot per minute (ft / min)</code></td></tr>
    <tr><td><code>foot per second (ft / s)</code></td></tr>
    <tr><td><code>inch per second (in / s)</code></td></tr>
    <tr><td><code>kilometer per hour (km / h)</code></td></tr>
    <tr><td><code>knot (nautical mile per hour)</code></td></tr>
    <tr><td><code>meter per second (m / s)</code></td></tr>
    <tr><td><code>mile per hour (mi / h)</code></td></tr>
    <tr><td><code>mile per minute (mi / min)</code></td></tr>
    <tr><td><code>mile per second (mi / s)</code></td></tr>
    <tr><td><code>radian per second (rad / s)</code></td></tr>
    <tr><td><code>revolution per minute (rpm) (r / min)</code></td></tr>
    <tr><td><code>rpm (revolution per minute) (r / min)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="viscosity-dynamic" data-category-name="VISCOSITY, DYNAMIC" data-unit-count="11">
<h2 id="viscosity-dynamic">VISCOSITY, DYNAMIC</h2>
<p class="unit-category-count">11 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>centipoise (cP)</code></td></tr>
    <tr><td><code>pascal second (Pa · s)</code></td></tr>
    <tr><td><code>poise (P)</code></td></tr>
    <tr><td><code>pound per foot hour [lb / (ft · h)]</code></td></tr>
    <tr><td><code>pound per foot second [lb / (ft · s)]</code></td></tr>
    <tr><td><code>pound-force second per square foot (lbf · s / ft2)</code></td></tr>
    <tr><td><code>pound-force second per square inch (lbf · s / in2)</code></td></tr>
    <tr><td><code>poundal second per square foot</code></td></tr>
    <tr><td><code>reciprocal pascal second (Pa · s)^-1</code></td></tr>
    <tr><td><code>rhe</code></td></tr>
    <tr><td><code>slug per foot second [slug / (ft · s)]</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="viscosity-kinematic" data-category-name="VISCOSITY, KINEMATIC" data-unit-count="4">
<h2 id="viscosity-kinematic">VISCOSITY, KINEMATIC</h2>
<p class="unit-category-count">4 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>centistokes (cSt)</code></td></tr>
    <tr><td><code>meter squared per second (m2 / s)</code></td></tr>
    <tr><td><code>square foot per second (ft2 / s)</code></td></tr>
    <tr><td><code>stokes (St)</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="volume" data-category-name="VOLUME (includes CAPACITY)" data-unit-count="28">
<h2 id="volume">VOLUME (includes CAPACITY)</h2>
<p class="unit-category-count">28 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>acre-foot (based on U.S. survey foot)</code></td></tr>
    <tr><td><code>barrel [for petroleum, 42 gallons (U.S.)](bbl)</code></td></tr>
    <tr><td><code>bushel (U.S.) (bu)</code></td></tr>
    <tr><td><code>cord (128 ft3)</code></td></tr>
    <tr><td><code>cubic foot (ft3)</code></td></tr>
    <tr><td><code>cubic inch (in3)</code></td></tr>
    <tr><td><code>cubic meter (m3)</code></td></tr>
    <tr><td><code>cubic mile (mi3)</code></td></tr>
    <tr><td><code>cubic yard (yd3)</code></td></tr>
    <tr><td><code>cup (U.S.)</code></td></tr>
    <tr><td><code>fluid ounce (U.S.) (fl oz)</code></td></tr>
    <tr><td><code>gallon (U.S.) (gal)</code></td></tr>
    <tr><td><code>gallon [Canadian and U.K. (Imperial)] (gal)</code></td></tr>
    <tr><td><code>gill (U.S.) (gi)</code></td></tr>
    <tr><td><code>gill [Canadian and U.K. (Imperial)] (gi)</code></td></tr>
    <tr><td><code>liter (L)</code></td></tr>
    <tr><td><code>milliliter (mL)</code></td></tr>
    <tr><td><code>ounce (U.S. fluid) (fl oz)</code></td></tr>
    <tr><td><code>ounce [Canadian and U.K. fluid (Imperial)] (fl oz)</code></td></tr>
    <tr><td><code>peck (U.S.) (pk)</code></td></tr>
    <tr><td><code>pint (U.S. dry) (dry pt)</code></td></tr>
    <tr><td><code>pint (U.S. liquid) (liq pt)</code></td></tr>
    <tr><td><code>quart (U.S. dry) (dry qt)</code></td></tr>
    <tr><td><code>quart (U.S. liquid) (liq qt)</code></td></tr>
    <tr><td><code>stere (st)</code></td></tr>
    <tr><td><code>tablespoon</code></td></tr>
    <tr><td><code>teaspoon</code></td></tr>
    <tr><td><code>ton, register</code></td></tr>
  </tbody>
</table>
</section>

<section class="unit-category" data-category="volume-divided-by-time" data-category-name="VOLUME DIVIDED BY TIME (includes FLOW)" data-unit-count="8">
<h2 id="volume-divided-by-time">VOLUME DIVIDED BY TIME (includes FLOW)</h2>
<p class="unit-category-count">8 supported units</p>
<table>
  <thead>
    <tr><th>Unit</th></tr>
  </thead>
  <tbody>
    <tr><td><code>cubic foot per minute (ft3 / min)</code></td></tr>
    <tr><td><code>cubic foot per second (ft3 / s)</code></td></tr>
    <tr><td><code>cubic inch per minute (in3 / min)</code></td></tr>
    <tr><td><code>cubic meter per second (m3 / s)</code></td></tr>
    <tr><td><code>cubic yard per minute (yd3 / min)</code></td></tr>
    <tr><td><code>gallon (U.S.) per day (gal / d)</code></td></tr>
    <tr><td><code>gallon (U.S.) per minute (gpm) (gal / min)</code></td></tr>
    <tr><td><code>liter per second (L / s)</code></td></tr>
  </tbody>
</table>
</section>

</div>
