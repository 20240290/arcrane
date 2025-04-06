"""
 Copyright 2024 Resurgo

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

class LazyLoader:
    """
    A class that will initialize the instances only when they are accessed for the first time.

    Args:
        None

    Returns:
        None 
    """

    #class variables
    _utility = None
    _arcrane = None

    @staticmethod
    def get_utility():
        """
        Static method to get the utility instance.

        Args:
            None

        Returns:
            Object : returns the Utilities object.
        """

        if LazyLoader._utility is None:
            from Utilities import Utilities  # Import only when needed
            LazyLoader._utility = Utilities()
        return LazyLoader._utility

    @staticmethod
    def get_arcrane():
        """
        Static method to get the arcrane instance.

        Args:
            None
            
        Returns:
            Object : returns the Arcrane object.
        """
                
        if LazyLoader._arcrane is None:
            from Arcrane import Arcrane  # Import only when needed
            LazyLoader._arcrane = Arcrane()
        return LazyLoader._arcrane


