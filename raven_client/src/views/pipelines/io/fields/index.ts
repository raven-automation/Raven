import { ColorFieldRenderer } from "./colorField";
import { DatetimeFieldRenderer } from "./datetimeField";
import { ListFieldRenderer } from "./listField";
import { NumberFieldRenderer } from "./numberField";
import { SelectFieldRenderer } from "./selectField";
import { StringFieldRenderer } from "./stringField";
import { SwitchFieldRenderer } from "./switchField";
import {
    FieldCreationFields,
    FieldCreationProps,
    IOFieldRenderer,
} from "./types";
export type { FieldCreationFields, FieldCreationProps, IOFieldRenderer };

export const FieldRenderers: { [key: string]: IOFieldRenderer<any> } = {
    string: StringFieldRenderer,
    number: NumberFieldRenderer,
    switch: SwitchFieldRenderer,
    select: SelectFieldRenderer,
    list: ListFieldRenderer,
    color: ColorFieldRenderer,
    datetime: DatetimeFieldRenderer,
};
