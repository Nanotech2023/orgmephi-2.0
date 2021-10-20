import { SimpleContest, TargetClass } from '@api/tasks/model'


export function getStatusDisplay( contest: SimpleContest | undefined ): string
{
    let contest1 = contest
    if ( contest1 === undefined )
        return ""

    let prefix = ""
    switch ( contest1?.status )
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
    if ( contest1.start_date === null )
        return prefix

    const year = new Date( contest1.start_date ).getFullYear()
    return year + ": " + prefix
}


export function getClassesForDisplay( contest: SimpleContest | undefined ): string
{
    let targetClasses = contest?.base_contest?.target_classes as TargetClass[]
    if ( targetClasses && targetClasses.length )
    {
        return `${ targetClasses[ 0 ].target_class }-${ targetClasses[ targetClasses.length - 1 ].target_class }`
    }
    return ""
}