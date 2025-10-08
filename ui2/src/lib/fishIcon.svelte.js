import plainFish from "./assets/fish-icons/fish-icon-1.svg";
import prettyFish1 from "./assets/fish-icons/fish-icon-2.svg";
import prettyFish2 from "./assets/fish-icons/fish-icon-3.svg";
import prettyFish3 from "./assets/fish-icons/fish-icon-4.svg";
import prettyFish4 from "./assets/fish-icons/fish-icon-5.svg";
import prettyFish5 from "./assets/fish-icons/fish-icon-6.svg";
import prettyFish6 from "./assets/fish-icons/fish-icon-7.svg";
import prettyFish7 from "./assets/fish-icons/fish-icon-8.svg";
import prettyFish8 from "./assets/fish-icons/fish-icon-9.svg";
import prettyFish9 from "./assets/fish-icons/fish-icon-10.svg";
import prettyFish10 from "./assets/fish-icons/fish-icon-11.svg";
import prettyFish11 from "./assets/fish-icons/fish-icon-12.svg";
import prettyFish12 from "./assets/fish-icons/fish-icon-13.svg";

import { stages } from "./state.svelte.js";


export { plainFish };

export const prettyFish = [prettyFish1, prettyFish2, prettyFish3, prettyFish4, prettyFish5, prettyFish6, prettyFish7, prettyFish8, prettyFish9, prettyFish10, prettyFish11, prettyFish12];


function randInt(max) {
    return Math.floor(Math.random() * max);
}

export function getUnusedFishIconIdx() {
    const inUse = [
        stages.camera?.iconIdx,
        stages.sedation?.iconIdx,
        stages.measurement?.iconIdx,
    ]

    let index = randInt(prettyFish.length);
    while (inUse.includes(index)) {
        index = randInt(prettyFish.length);
    }

    return index;
}

export function getRandomFishIcon() {
    let index = randInt(prettyFish.length);
    return prettyFish[index];
}