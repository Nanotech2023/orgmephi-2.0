export enum SchoolType
{
    school = 'Школа',
    lyceum = 'Лицей',
    gymnasium = 'Гимназия'

}


export interface Education
{
    isAbroadSchool: boolean
    region: string
    city: string
    type: SchoolType
    number: number
    name: string
    class: number
}


export const emptyEducation: Education = {
    isAbroadSchool: false,
    region: '',
    city: '',
    type: SchoolType.school,
    number: 0,
    name: '',
    class: 5
}