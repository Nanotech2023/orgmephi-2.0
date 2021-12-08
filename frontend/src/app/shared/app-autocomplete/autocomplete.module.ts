import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { AutocompleteComponent } from './autocomplete.component'
import { AutocompleteDirective } from './autocomplete.directive'
import { AutocompleteContentDirective } from './autocomplete-content.directive'
import { AutocompleteOptionComponent } from '@/shared/app-autocomplete/autocomplete-option.component';
import { FilterPipe } from './filter.pipe'


const COMPONENTS = [
    AutocompleteComponent,
    AutocompleteDirective,
    AutocompleteContentDirective,
    AutocompleteOptionComponent,
    FilterPipe
]


@NgModule( {
    imports: [ CommonModule ],
    declarations: [ COMPONENTS ],
    exports: [ COMPONENTS ]
} )
export class AutocompleteModule
{
}