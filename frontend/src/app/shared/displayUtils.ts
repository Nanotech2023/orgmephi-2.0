import { Contest, SimpleContest, TargetClass } from '@api/tasks/model'


export function getStatusDisplay( contest?: Contest ): string
{
    if ( contest === undefined )
        return ""

    let prefix = ""
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
    {
        const year = new Date( contest.academic_year ).getFullYear()
        return year + ": " + prefix
    }
    else return prefix
}


export function getClassesForDisplay( contest?: Contest ): string
{
    let targetClasses = contest?.base_contest?.target_classes as TargetClass[]
    if ( targetClasses && targetClasses.length )
    {
        return `${ targetClasses[ 0 ].target_class }-${ targetClasses[ targetClasses.length - 1 ].target_class }`
    }
    return ""
}