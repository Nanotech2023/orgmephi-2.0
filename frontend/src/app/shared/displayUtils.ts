import { Contest, SimpleContest, TargetClass } from '@api/tasks/model'
import { DocumentTypeEnum, GenderEnum, LocationTypeEnum, SchoolTypeEnum } from '@api/users/models'
import { SubjectEnum } from '@api/shared/model'


export function getGenderDisplay( genderEnum: GenderEnum ): string
{
    switch ( genderEnum )
    {
        case 'Male':
            return 'Мужской'
        case 'Female':
            return 'Женский'
    }
}

export function getDocumentDisplay( documentTypeEnum: DocumentTypeEnum ): string
{
    switch ( documentTypeEnum )
    {
        case 'RFPassport':
            return "Паспорт гражданина РФ"
        case 'RfInternationalPassport':
            return "Заграничный паспорт гражданина РФ"
        case 'BirthCertificate':
            return "Свидетельство о рождении гражданина РФ"
        case 'ForeignPassport':
            return "Паспорт гражданина иностранного государства"
        case 'OtherDocument':
            return "Другой документ"
    }
}

export function getStatusDisplay( contest?: Contest ): string
{
    let prefix = ""

    if ( contest === undefined )
        return prefix

    switch ( contest?.status )
    {
        case SimpleContest.StatusEnum.WillStartSoon:
            prefix = "Скоро начнётся"
            break
        case SimpleContest.StatusEnum.InProgress:
            prefix = "Проходит"
            break
        case SimpleContest.StatusEnum.Finished:
            prefix = "Олимпиада завершена"
            break
    }

    if ( contest.academic_year )
        return contest.academic_year + ": " + prefix

    return prefix
}


export function getClassesForDisplay( contest?: Contest ): string
{
    let targetClasses = contest?.base_contest?.target_classes as TargetClass[]
    if ( targetClasses )
        if ( targetClasses.length == 1 )
        {
            return `${ targetClasses[ 0 ].target_class }`
        }
        else if ( targetClasses.length > 1 )
        {
            return `${ targetClasses[ 0 ].target_class }-${ targetClasses[ targetClasses.length - 1 ].target_class }`
        }
    return ""
}

export function getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
{
    switch ( schoolType )
    {
        case 'School':
            return "Школа"
        case 'Lyceum':
            return "Лицей"
        case 'Gymnasium':
            return "Гимназия"
        case 'EducationCenter':
            return "Образовательный центр"
        case 'NightSchool':
            return "Вечерняя школа"
        case 'Technical':
            return "Техническое"
        case 'External':
            return "Внешнее образование"
        case 'Collage':
            return "Колледж"
        case 'ProfTech':
            return "ProfTech"
        case 'University':
            return "Университет"
        case 'Correctional':
            return "Учебно-исправительный центр"
        case 'Other':
            return "Другое"
    }
}

export function getSubjectDisplay( subject?: SubjectEnum ): string
{
    switch ( subject )
    {
        case 'Physics':
            return "Физика"
        case 'Informatics':
            return "Информатика"
        case 'Natural Sciences':
            return "Естественные науки"
        case 'Engineering Sciences':
            return "Инженерные науки"
        case 'Math':
            return "Математика"
        case 'Other':
        case undefined:
            return "Другое"
    }
}

export function getLocationDisplay( locationType: LocationTypeEnum ): string
{
    switch ( locationType )
    {
        case 'Russian':
            return "Россия"
        case 'Foreign':
            return "Другая страна"
    }

}