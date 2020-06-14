import React, {StyleSheet, Dimensions, PixelRatio} from "react-native";
const {width, height, scale} = Dimensions.get("window"),
    vw = width / 100,
    vh = height / 100,
    vmin = Math.min(vw, vh),
    vmax = Math.max(vw, vh);

export default StyleSheet.create({
    "table-field-list tbody tr td": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list tbody tr th": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list thead tr th": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list thead tr td": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list tfoot tr th": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list tfoot tr td": {
        "border": "none",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table>tbody>tr:last-child>td": {
        "paddingBottom": "10px ! important"
    },
    "table>tfoot>tr:last-child>td": {
        "paddingBottom": "10px ! important"
    },
    "table-field-list thead tr th:first-child": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list tbody tr td:first-child": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list tfoot tr td:first-child": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "table-field-list thead tr th:last-child": {
        "paddingRight": 0,
        "paddingBottom": 0
    },
    "table-field-list tbody tr td:last-child": {
        "paddingRight": 0,
        "paddingBottom": 0
    },
    "table-field-list tfoot tr td:last-child": {
        "paddingRight": 0,
        "paddingBottom": 0
    },
    "table-field-list": {
        "marginTop": 10
    },
    "active-menu": {
        "color": "red !important"
    },
    "text-user": {
        "color": "#2196F3 !important",
        "cursor": "pointer"
    },
    "card card-header": {
        "borderBottom": "1px solid #EEEEEE !important"
    },
    "board-status": {
        "fontSize": 11,
        "color": "#FFFFFF",
        "paddingTop": 1,
        "paddingRight": 5,
        "paddingBottom": 1,
        "paddingLeft": 5
    },
    "rating-down-active": {
        "color": "red"
    },
    "rating-up-active": {
        "color": "#4CAF50"
    },
    "rating-none-active": {
        "color": "#2196F3"
    },
    "rating-up": {
        "cursor": "pointer"
    },
    "rating-down": {
        "cursor": "pointer"
    },
    "rating-none": {
        "cursor": "pointer"
    },
    "rating-up:hover": {
        "color": "#4CAF50"
    },
    "rating-down:hover": {
        "color": "red"
    },
    "rating-none:hover": {
        "color": "#2196F3"
    }
});