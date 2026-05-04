/**
 * 行程規劃用名單（與首頁口袋店 id 對齊可擴充）。
 * schedule：以 JavaScript getDay() 為鍵 — 0 週日 … 6 週六；null 表示未建檔（頁面會提示改查地圖）。
 * closed：當日公休。from / to：參考時段（24h 字串），仍請以 Google 地圖為準。
 */
window.PLANNER_PLACES = [
  {
    id: "hammer",
    name: "錘子咖啡",
    mapQuery: "錘子咖啡 士林 台北",
    district: "士林",
    landmark: "鄰近士林官邸／士林夜市／北美館",
    tags: ["獨立", "手沖", "外帶友善", "巷弄"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "假日士林夜市周邊人流高",
    intro: "清爽白色小店，豆子選線直白。"
  },
  {
    id: "coffee-flair",
    name: "COFFEE FLAIR",
    mapQuery: "COFFEE FLAIR 台北",
    district: "中山",
    landmark: "鄰近圓山／花博／中山國小站",
    tags: ["義式", "自烘", "甜點", "吧檯"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "晴光商圈假日午後中等",
    intro: "競賽系譜的吧台節奏；適合喜歡香氣路線。"
  },
  {
    id: "d23",
    name: "D23 Coffee Roasters",
    mapQuery: "D23 Coffee Roasters 台北",
    district: "中山",
    landmark: "鄰近松江南京／小巨蛋／行天宮",
    tags: ["自烘", "工業風", "性格店", "獨立"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "展演日前後小巨蛋人潮明顯",
    intro: "街角性格店，座位珍稀。"
  },
  {
    id: "luguo",
    name: "爐鍋咖啡",
    mapQuery: "爐鍋咖啡 小藝埕 台北",
    district: "大同",
    landmark: "鄰近大稻埕／迪化街／北門",
    tags: ["老城", "散步", "自烘", "安靜"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "迪化街假日觀光客多",
    intro: "小藝埕動線易接老城散步。"
  },
  {
    id: "cho",
    name: "町‧如固咖啡 CHO café",
    mapQuery: "町‧如固咖啡 CHO café 台北",
    district: "萬華",
    landmark: "鄰近西門町／龍山寺／北門",
    tags: ["老屋", "老宅", "精品", "巷弄"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "西門週末午後人潮偏高",
    intro: "六十年老宅裡的烘焙與沖煮。"
  },
  {
    id: "beanroom",
    name: "(beanroom)",
    mapQuery: "(beanroom) 台北",
    district: "大安",
    landmark: "鄰近東區／忠孝復興／SOGO",
    tags: ["策展", "豆列", "東區", "獨立"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "東區假日下午至晚上人流高",
    intro: "配方豆與莊園豆策展式呈現。"
  },
  {
    id: "vwi",
    name: "VWI by CHADWANG",
    mapQuery: "VWI by CHADWANG 台北",
    district: "大安",
    landmark: "鄰近東區／忠孝復興／SOGO",
    tags: ["沖煮", "冠軍", "儀式感", "東區"],
    closedIfMonday: false,
    schedule: null,
    crowdAreaNote: "東區假日下午至晚上人流高",
    intro: "白色三角窗與吧台儀式感。"
  },
  {
    id: "oasis",
    name: "Oasis Coffee Roasters",
    mapQuery: "Oasis Coffee Roasters 台北",
    district: "大安",
    landmark: "鄰近信義安和／永康／大安路",
    tags: ["自烘", "綠意", "安全牌", "獨立"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "永康商圈假日中等偏高",
    intro: "風味清楚，多款豆子輪替。"
  },
  {
    id: "orbit",
    name: "迴廊 Orbit Coffee",
    mapQuery: "迴廊 Orbit Coffee 台北",
    district: "大安",
    landmark: "鄰近信義安和／永康／大安路",
    tags: ["摩登復古", "深夜", "獨立", "咖啡"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "巷內店較不受大馬路人潮直接影響",
    intro: "建議動線第一站；摩登復古節奏。"
  },
  {
    id: "soundsgood",
    name: "聲色 Sounds Good",
    mapQuery: "聲色 Sounds Good 台北",
    district: "大安",
    landmark: "鄰近大安森林公園／師大／新生南路",
    tags: ["黑膠", "深夜", "音樂", "獨立"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "週末午後公園周邊散步人潮多",
    intro: "黑膠選曲；適合第二站。"
  },
  {
    id: "wu",
    name: "蕪咖啡",
    mapQuery: "蕪咖啡 台北",
    district: "大安",
    landmark: "鄰近大安森林公園／師大／新生南路",
    tags: ["義式", "深夜", "獨立", "收尾"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "巷弄店相對商圈核心区安靜",
    intro: "動線第三站；深夜對話友善。"
  },
  {
    id: "single-origin",
    name: "Single Origin espresso & roast",
    mapQuery: "Single Origin espresso & roast 台北",
    district: "信義",
    landmark: "鄰近台北101／世貿／象山步道口",
    tags: ["單一產區", "老宅", "信義", "窗景"],
    closedIfMonday: true,
    schedule: null,
    crowdAreaNote: "信義計畫區一帶假日下午人潮高",
    intro: "吳興街老宅二樓；產區敘事清楚。"
  }
];
